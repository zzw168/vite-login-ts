from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 配置，允许前端访问后端
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源访问（生产环境建议指定具体来源）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义数据模型
class Record(BaseModel):
    id: int
    name: str
    age: int
    email: str
    avatar: str = None  # 可选字段，默认值为 None

class User(BaseModel):
    name: str
    email: str
    phone: str
    avatar: Optional[str] = None
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# 模拟数据库
records = [
    Record(id=1, name="张三", age=28, email="zhangsan@example.com", avatar="/images/1.png"),
    Record(id=2, name="李四", age=32, email="lisi@example.com", avatar="/images/9.png"),
]

users = [
    {"username": "admin", "password": "1234"},
    {"username": "user", "password": "1234"},
]

# 登录接口
@app.post("/api/login")
async def login(login_request: LoginRequest):
    for user in users:
        if user["username"] == login_request.username and user["password"] == login_request.password:
            return {"message": "Login successful", "role": "admin" if login_request.username == "admin" else "user"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

# 保存用户资料
@app.post("/api/saveUser")
async def save_user(user: User):
    # 模拟保存用户资料的逻辑
    print(f"Saving user: {user}")
    # 这里可以添加实际的数据库保存逻辑
    return {"message": "User saved successfully", "user": user}


# 获取所有记录
@app.get("/records", response_model=List[Record])
async def get_records():
    return records

# 获取单条记录
@app.get("/records/{record_id}", response_model=Record)
async def get_record(record_id: int):
    """
    根据记录 ID 获取单条记录
    """
    # 在记录列表中查找对应 ID 的记录
    record = next((r for r in records if r.id == record_id), None)

    # 如果记录不存在，返回 404 错误
    if record is None:
        raise HTTPException(status_code=404, detail="记录未找到")

    return record


# 新增记录
@app.post("/records", response_model=Record)
async def add_record(record: Record):
    # 检查 ID 是否重复
    if any(r.id == record.id for r in records):
        raise HTTPException(status_code=400, detail="记录 ID 已存在")
    records.append(record)
    return record

# 删除单条记录
@app.delete("/records/{record_id}", status_code=204)
async def delete_record(record_id: int):
    global records
    # 检查记录是否存在
    record = next((r for r in records if r.id == record_id), None)
    if not record:
        raise HTTPException(status_code=404, detail="记录未找到")
    records = [r for r in records if r.id != record_id]
    return

# 批量删除记录
class BatchDeleteRequest(BaseModel):
    record_ids: List[int]


@app.post("/records/batch-delete")
async def batch_delete_records(request: BatchDeleteRequest):
    """
    批量删除记录
    """
    global records
    if not request.record_ids:
        raise HTTPException(status_code=400, detail="record_ids 列表不能为空")

    original_count = len(records)
    records = [record for record in records if record.id not in request.record_ids]

    deleted_count = original_count - len(records)
    return {"message": f"成功删除 {deleted_count} 条记录"}

# 编辑记录
@app.put("/records/{record_id}", response_model=Record)
async def update_record(record_id: int, updated_record: Record):
    # 查找记录是否存在
    index = next((i for i, r in enumerate(records) if r.id == record_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="记录未找到")

    # 更新记录内容
    records[index] = updated_record
    return updated_record


# 启动服务的入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8086)
