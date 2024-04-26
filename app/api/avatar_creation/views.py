from datetime import datetime
from fastapi import FastAPI, HTTPException, APIRouter, Depends, Body, Query, Response, UploadFile
from uuid import UUID
from typing import List
from app.api.avatar_creation.api_models import (
    AvatarEmail,
    AvatarGenerate,
    AvatarGenerateManual,
    AvatarGmailBase,
    AvatarPlatformAdd,
    AvatarPlatformBase,
    AvatarResponse,
    AvatarBaseInsert,
    FacebookAcount,
    GoogleAccount,
    InstaAccount,
)
from app.api.avatar_creation import service
from sqlalchemy.orm import Session
from app.api.commons.account_creation import create_gmail_account
from app.api.commons.facebook_account import create_facebook_account, create_facebook_account_phone
from app.api.commons.gmail_fetch import fetch_instagram_codes
from app.api.commons.insta_account import create_insta_account
from app.api.jobs.service import initiate_avatar_generation
from app.database.session import get_db
from app.api.commons.api_models import ResponseEnvelope, status

from app.api.commons.api_models import (
    GenericFilterParameters,
    OrderParameters,
    Pagination,
    PaginationParameters,
    ResponseEnvelope,
)

router = APIRouter()


@router.post(
    path="",
    response_model=ResponseEnvelope,
    operation_id="createAvatarmanual",
    summary="Create Avatar Data.",
    status_code=status.HTTP_201_CREATED,
)
def create(
    db: Session = Depends(get_db),
    avatar: AvatarGenerateManual = Body(...),
):
    Avatar_response = service.generate_users_manually(db, avatar)
    response_data = AvatarResponse.from_orm(Avatar_response)
    AvatarGroup_response = ResponseEnvelope(data=response_data)
    return AvatarGroup_response

@router.post(
    path="/gmail",
    response_model=ResponseEnvelope,
    operation_id="createAvatarmanualgmail",
    summary="Create Avatar Data.",
    status_code=status.HTTP_201_CREATED,
)
def create_avatar_gmail(
    db: Session = Depends(get_db),
    avatar: AvatarEmail = Body(...),
):
    Avatar_response = service.generate_user_email(db, avatar)
    AvatarGroup_response = ResponseEnvelope(data=avatar)
    return AvatarGroup_response

@router.post(
    path="/platform",
    response_model=ResponseEnvelope,
    operation_id="createAvatarmanualplatform",
    summary="Create Avatar Data.",
    status_code=status.HTTP_201_CREATED,
)
def create_avatar_platform(
    db: Session = Depends(get_db),
    avatar: AvatarPlatformAdd = Body(...),
):
    Avatar_response = service.generate_user_platform(db, avatar)
    AvatarGroup_response = ResponseEnvelope(data=avatar)
    return AvatarGroup_response
# @router.post(
#     path="",
#     response_model=ResponseEnvelope,
#     operation_id="createAvatar",
#     summary="Create Avatar Data.",
#     status_code=status.HTTP_201_CREATED,
# )
# def create(
#     db: Session = Depends(get_db),
#     avatar: AvatarBaseInsert = Body(...),
# ):
#     AvatarGroup_response = service.create_avatar(db, avatar)
#     response_data = AvatarResponse.from_orm(AvatarGroup_response)
#     AvatarGroup_response = ResponseEnvelope(data=response_data)
#     return AvatarGroup_response


@router.get(
    path="",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listAvatar",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_avatar(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_avatars(
        session,
        pagination_params,
        order_params,
        filter_params,
    )
    response_data_list=[]
    current_year = datetime.now().year
    for elem in response:
        # elem.birthdate= datetime(elem.birthdate)

        response_data = AvatarResponse.from_orm(elem)
        response_data.a_gender=elem.gender.desc_en
        response_data.a_age=int(current_year-elem.birthdate.year)
        response_data.a_avatar_group=elem.avatar_group.group_name
        response_data.a_country=elem.country.desc_en
        response_data.a_relationship_status=elem.relationship_status.desc_en
        response_data.a_nationality=elem.nationality.desc_en
        response_data.photo=elem.photo
        response_data_list.append(response_data)

    response = ResponseEnvelope[List[AvatarResponse]](
        data=response_data_list,
        pagination=Pagination(
            size=pagination_params.size,
            page=pagination_params.page,
            total_pages=total_pages,
            total_elements=total_elements,
            order_by=order_params.order_by,
        ),
    )
    return response

@router.get(
    path="/gmail",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listAvatarbygmail",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_gmail_avatar(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_gmail_avatars(
        session,
        pagination_params,
        order_params,
        filter_params,
    )
    response_data_list=[]
    current_year = datetime.now().year
    for elem in response:
        # elem.birthdate= datetime(elem.birthdate)

        response_data = AvatarGmailBase.from_orm(elem)
        response_data.id=elem.avatar_id
        response_data.provider=elem.email_provider.desc_en
        response_data.email_provider_id=elem.email_provider.desc_en
   
        response_data_list.append(response_data)

    response = ResponseEnvelope[List[AvatarGmailBase]](
        data=response_data_list,
        pagination=Pagination(
            size=pagination_params.size,
            page=pagination_params.page,
            total_pages=total_pages,
            total_elements=total_elements,
            order_by=order_params.order_by,
        ),
    )
    return response
@router.get(
    path="/platform",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listAvatarbyplatform",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_platform_avatar(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_platform_avatars(
        session,
        pagination_params,
        order_params,
        filter_params,
    )
    response_data_list=[]
    current_year = datetime.now().year
    for elem in response:
        # elem.birthdate= datetime(elem.birthdate)

        response_data = AvatarPlatformBase.from_orm(elem)
        response_data.id=elem.avatar_id
        response_data.username=elem.email.split('@')[0]
        response_data.platform_name=elem.platform.desc_en
        response_data.platform_id=elem.platform_id
        response_data.is_valid=True
        response_data_list.append(response_data)

    response = ResponseEnvelope[List[AvatarPlatformBase]](
        data=response_data_list,
        pagination=Pagination(
            size=pagination_params.size,
            page=pagination_params.page,
            total_pages=total_pages,
            total_elements=total_elements,
            order_by=order_params.order_by,
        ),
    )
    return response
@router.get(
    path="/scheduler_no",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listAvatar",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_avatar_by_scheduler(
    scheduler_no:UUID,
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_avatars_by_scheduler_no_api(
        session,
        pagination_params,
        order_params,
        filter_params,
        scheduler_no
    )
    current_year = datetime.now().year

    response_data_list=[]
    for elem in response:
        
        response_data = AvatarResponse.from_orm(elem)
        response_data.a_gender=elem.gender.desc_en
        response_data.a_age=int(current_year-elem.birthdate.year)
        response_data.a_avatar_group=elem.avatar_group.group_name
        response_data.a_country=elem.country.desc_en
        response_data.a_relationship_status=elem.relationship_status.desc_en
        response_data.a_nationality=elem.nationality.desc_en
        response_data_list.append(response_data)

    response = ResponseEnvelope[List[AvatarResponse]](
        data=response_data_list,
        pagination=Pagination(
            size=pagination_params.size,
            page=pagination_params.page,
            total_pages=total_pages,
            total_elements=total_elements,
            order_by=order_params.order_by,
        ),
    )
    return response


@router.get(
    path="/{id}",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="getAvatarById",
    summary="Retrieve Avatar data by id.",
    status_code=status.HTTP_200_OK,
)
def read_Avatar_by_id(
    id: UUID,
    session: Session = Depends(get_db),
):
    """Endpoint for retrieving single Client info by id."""

    response = service.get_avatar_by_id(session, id)

    response_data = AvatarResponse.from_orm(response)

    response = ResponseEnvelope[AvatarResponse](data=response_data)

    return response


@router.delete(
    path="/bulk-delete",
    response_model=ResponseEnvelope,
    operation_id="deletebulkAvatarById",
    summary="Delete bulk Avatar Data by id.",
    status_code=status.HTTP_200_OK,
)
def delete_Avatar(
    id: List[int],
    session: Session = Depends(get_db),
):
    """Endpoint for deleting a single AvatarGroup data by id."""

    service.delete_avatar_bulk(session, id)
    return ResponseEnvelope(data="Record deleted Successfully")

@router.put(
    path="",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="putAvatarById",
    summary="Update Avatar  by id.",
    status_code=status.HTTP_200_OK,
)
def update_Avatar(
    id: int,
    AvatarGroup_update: AvatarBaseInsert = Body(...),
    session: Session = Depends(get_db),
):
    """Endpoint for updating single AvatarGroup   Data by id."""

    response = service.update_avatar(session, id, AvatarGroup_update)
    response_data = AvatarResponse.from_orm(response)
    response = ResponseEnvelope(data=response_data)
    return response


# @router.post(
#     path="/generateuser",
#     response_model=ResponseEnvelope,
#     response_model_exclude_none=True,
#     operation_id="generate user",
#     summary="posy Avatar auto",
#     status_code=status.HTTP_200_OK
# )
# def generate_user(
#     session: Session = Depends(get_db),
#     number_of_users: int = Query(5, description="Number of users to generate"),
#     country: str = Query("USA", description="Country for generating names"),
#     group: str = Query(None, description="Group to which the user belongs"),  # Query parameter for group
#     platform: str = Query(None, description="Platform associated with the user"),  # Query parameter for platform
#     nationality: str = Query(None, description="Nationality of the user") ,
#     language: str = Query(None, description="Primary language of the user"),  # New parameter for language
#     gender: str = Query(None, description="Gender of generated users"),  # New parameter for Gender
#     style_id: str = Query("default", description="Style ID for profile picture generation")
# ):
#     users = service.generate_users(session, number_of_users, country, group, platform, nationality, language, gender, style_id)
#     response_data = [AvatarResponse.from_orm(user) for user in users]
#     return ResponseEnvelope(data=response_data)

@router.post(
    path="/generate-avatars",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="generate avatar",
    summary="post Avatar auto",
    status_code=status.HTTP_200_OK,
)
def generate_user(
    session: Session = Depends(get_db),
    number_of_users: int = Query(5, description="Number of users to generate"),
    country: str = Query("USA", description="Country for generating names"),
    group: str = Query(None, description="Group to which the user belongs"),  # Query parameter for group
    platform: str = Query(None, description="Platform associated with the user"),  # Query parameter for platform
    nationality: str = Query(None, description="Nationality of the user") ,
    language: str = Query(None, description="Primary language of the user"),  # New parameter for language
    gender: str = Query(None, description="Gender of generated users"),  # New parameter for Gender
    style_id: str = Query("default", description="Style ID for profile picture generation")
):
    users=service.generate_users(session,number_of_users,country,group,platform,nationality,language,gender,style_id)
    response_data = users
    return ResponseEnvelope(data=response_data)
@router.post(
    path="/v2/generate-avatars",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="generate avatar v2",
    summary="post Avatar auto v2",
    status_code=status.HTTP_200_OK,
)
def generate_user(
    request_data: AvatarGenerate = Body(...),  # Using Body to parse JSON body
    session: Session = Depends(get_db)
):
    # Now, pass the model instance directly to your service layer
    try:
        initialize_scheduler=initiate_avatar_generation(session,request_data.dict())
        # response_data = service.generate_users_v2(session,request_data )
        return ResponseEnvelope(data=initialize_scheduler)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    path="/createaccount",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="generate user",
    summary="post Avatar auto",
    status_code=status.HTTP_200_OK,
)
def generate_user(
    session: Session = Depends(get_db),
    user: GoogleAccount = Body(...),
):
    users = create_gmail_account(
        user.firstName,
        user.lastName,
        user.userName,
        user.birthday,
        user.Gender,
        user.password,
    )
    response_data = user
    return ResponseEnvelope(data=response_data)

@router.post(
    path="/createinstaaccount",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="insta user",
    summary="post insta auto",
    status_code=status.HTTP_200_OK,
)
def generate_user(
    session: Session = Depends(get_db),
    user: InstaAccount = Body(...),
):
    # otp=fetch_instagram_codes(user.email,'djcz kqbt nzfj qwrk')
    # otp_codes=otp['instagram_codes']
    # size=len(otp_codes)
    # opt=otp_codes[size-1]
    users = create_insta_account(
        user.email,
        user.fullName,
        user.userName,
        user.password,
        user.birthday,
        user.appPassword
    )
    response_data = user
    return ResponseEnvelope(data=response_data)


@router.post(
    path="/create-facebook-account",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="facebook user",
    summary="post facebook auto",
    status_code=status.HTTP_200_OK,
)
def generate_user(
    session: Session = Depends(get_db),
    user: FacebookAcount = Body(...),
):
    # otp=fetch_instagram_codes(user.email,'djcz kqbt nzfj qwrk')
    # otp_codes=otp['instagram_codes']
    # size=len(otp_codes)
    # opt=otp_codes[size-1]
    users = create_facebook_account(
        user.email,
        user.firstName,
        user.surName,
        user.password,
        user.birthday
    )
    response_data = user
    return ResponseEnvelope(data=response_data)

@router.post(
    path="/uploadfile/",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="upload image",
    summary="upload image",
    status_code=status.HTTP_200_OK,
)
async def create_upload_file(
    session: Session = Depends(get_db),
    id:int=Query(...),
    file: UploadFile=None
    ):
    profile_picture=service.upload_avatar_image(session,id,file.content_type,file.filename)
    if profile_picture is True:
        return ResponseEnvelope(data="Image uploaded successfully")
    else:
        raise  HTTPException(status_code=400,detail="Image upload Failed")