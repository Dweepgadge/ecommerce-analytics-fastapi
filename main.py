from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import pandas as pd
from datetime import datetime, timedelta
import jwt
import bcrypt

# SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ----------------- 1. CONFIGURATION & JWT SETTINGS -----------------
DATABASE_URL = "sqlite:///./orders.db"
SECRET_KEY = "supersecretcompanykey123"  # Interview: "Production me ye .env file me rehti hai"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Token extract karne ke liye FastAPI ka tool
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ----------------- 2. DATABASE MODELS -----------------
# A. Users Table
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# B. Orders Table
class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    total_bill = Column(Float)

Base.metadata.create_all(bind=engine)


# ----------------- 3. PYDANTIC SCHEMAS -----------------
class UserRegister(BaseModel):
    username: str
    password: str

class OrderCreate(BaseModel):
    product_name: str
    price: float
    quantity: int

class OrderResponse(OrderCreate):
    id: int
    total_bill: float
    class Config:
        from_attributes = True


# ----------------- 4. HELPER FUNCTIONS (Security) -----------------
# Password Hash karna
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Password Verify karna
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# JWT Token banana
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Database Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Interview Favorite: Dependency jo token verify karke user return karegi
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token Expire ho chuka hai ya Invalid hai")

    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User nahi mila")
    return user


# ----------------- 5. FASTAPI APP & ROUTES -----------------
app = FastAPI()
    # HomePage par seedhe Dashboard dikhao
# HomePage par seedhe Dashboard ka HTML bhej do
@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

app = FastAPI()

# CORS Middleware (Frontend ko backend se baat karne ki permission deta hai)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production me yahan specific website ka domain aata hai
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 1. User Register Route
@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Check karo user pehle se exist toh nahi karta
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Ye username pehle se registered hai!")
    
    # Password hash karke DB me save karo
    new_user = UserDB(username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": f"User {user.username} successfully register ho gaya!"}


# 2. Login Route (Generates JWT Token)
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Galat Username ya Password!")
    
    # Token generate karo
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# 3. Public Route: Saare Orders dekhna (Koi bhi dekh sakta hai)
@app.get("/orders/")
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderDB).all()
    return {"total_count": len(orders), "data": orders}


# 4. PROTECTED ROUTE: Order Delete karna (Sirf Logged-in User hi kar sakta hai!)
# Notice: 'current_user: UserDB = Depends(get_current_user)' ye guard ki tarah kaam kar raha hai!
@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order nahi mila!")
    
    db.delete(order)
    db.commit()
    return {"message": f"Order {order_id} delete kar diya gaya by {current_user.username}!"}


# 5. PROTECTED ROUTE: Naya Order create karna (Sirf Logged-in User)
@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    db_order = OrderDB(
        product_name=order.product_name,
        price=order.price,
        quantity=order.quantity,
        total_bill=order.price * order.quantity
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Analytics Route (Jo Pandas se metrics calculate karta hai)
@app.get("/analytics/")
def get_analytics(db: Session = Depends(get_db)):
    orders = db.query(OrderDB).all()
    if not orders:
        return {
            "total_revenue": 0,
            "average_order_value": 0,
            "total_items_sold": 0
        }
    
    # Pandas DataFrame banaya
    data = [{"price": o.price, "quantity": o.quantity, "total_bill": o.total_bill} for o in orders]
    df = pd.DataFrame(data)
    
    return {
        "total_revenue": float(df["total_bill"].sum()),
        "average_order_value": round(float(df["total_bill"].mean()), 2),
        "total_items_sold": int(df["quantity"].sum())
    }
