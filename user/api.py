from fastapi import APIRouter,Depends,UploadFile,File
from . models import *
from . pydantic_models import usercreate,deleteuser,updateuser,personecreate,loginuser,Token
from fastapi.responses import JSONResponse,HTMLResponse
from passlib.context import CryptContext
import os
from datetime import datetime
from fastapi_login import LoginManager



SECRET = 'your-secret-key'

app = APIRouter()
pwd_context= CryptContext(schemes=['bcrypt'],deprecated='auto')
manager = LoginManager(SECRET, token_url='/auth/token')


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/create_user")
async def create_user(data:personecreate
                      ):

    if await Persone.exists(email=data.email):
        return {"status":False, "message":"Email Already Exists"}
    else:
       person_obj =  await Persone.create(email = data.email,
                             password = get_password_hash(data.password))
       return person_obj

@manager.user_loader()
async def load_user(email: str):
    if await Persone.exists(email=email):
        user = await Persone.get(email=email)
        return user

@app.post('/auth/token')
async def login(data: loginuser):
    email = data.email

    user = await load_user(email)
    if not user:
        raise JSONResponse({'status':False,'message':'User Not Ragister'}, status_code=403) 
    
    elif not verify_password(data.password,user.password):
        return JSONResponse({"status":False, "message":"Invalid Password"}, status_code=403)

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.post("/")
async def ragistration(data:usercreate = Depends(),
                       image:UploadFile = File(...)):
    phone_number = str(data.mobile)

    if len(phone_number) != 10:
        return {"status":False, "message":"Invalid Number"}
    if await User.exists(mobile=phone_number):
        return {"status":False, "message":"Phone Number Already Exists"}
    elif await User.exists(email=data.email):
        return {"status":False, "message":"Email Already Exists"}
    else:
        FILEPATH = "static/image/"
        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]    
        if extension in ["png","JPG","jpeg"]:
            return {"status":"eroor","detials":"Filen Extension Not Allowed"}
        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename + "_" + str(dt_timestamp) + "." +  extension
        genrated_name = FILEPATH + modified_image_name
        file_content = await image.read()

        with open(genrated_name,"wb") as file:
            file.write(file_content)

            file.close()

    valid_hobbies = []

    for hobby_str in data.hobby:
        try:
            hobby = Hobby(hobby_str)
            valid_hobbies.append(hobby)
        except ValueError:
            print(f"invalid hobby {hobby_str}")    
    user_obj = await User.create(
           name = data.name,
           email= data.email,
           mobile = data.mobile,
           country = data.country,
           image = genrated_name,
           city = data.city,
           state = data.state,
           gender = data.gender,
           hobby = data.hobby

       )    
     
    return user_obj
        



@app.delete("/delete/")
async def delete_user(data:deleteuser):
    await User.filter(id = data.id).delete()
    return {"status":True, "message":"User Delete Sucessfully"}

        

@app.put("/update_user")
async def ragistration(data:updateuser = Depends(),
                       image:UploadFile = File(...)):
    phone_number = str(data.mobile)

    if len(phone_number) != 10:
        return {"status":False, "message":"Invalid Number"}
    if await User.exists(mobile=phone_number):
        return {"status":False, "message":"Phone Number Already Exists"}
    elif await User.exists(email=data.email):
        return {"status":False, "message":"Email Already Exists"}
    else:
        FILEPATH = "static/image/"
        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]    
        if extension in ["png","JPG","jpeg"]:
            return {"status":"eroor","detials":"Filen Extension Not Allowed"}
        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename + "_" + str(dt_timestamp) + "." +  extension
        genrated_name = FILEPATH + modified_image_name
        file_content = await image.read()

        with open(genrated_name,"wb") as file:
            file.write(file_content)

            file.close()

    valid_hobbies = []

    for hobby_str in data.hobby:
        try:
            hobby = Hobby(hobby_str)
            valid_hobbies.append(hobby)
        except ValueError:
            print(f"invalid hobby {hobby_str}")    
    user_obj = await User.filter(id=data.id).update(
           name = data.name,
           email= data.email,
           mobile = data.mobile,
           country = data.country,
           image = genrated_name,
           city = data.city,
           state = data.state,
           gender = data.gender,
           hobby = data.hobby

       )    
     
    return {"message":"User Update Sucessfully" , "user_obj":user_obj}
        
