from fastapi import FastAPI,HTTPException,APIRouter,Depends,Body,Response
from uuid import UUID
from typing import List
from app.api.avatar_groups.api_models import AvatarGroupResponse,AvatarGroupBaseInsert
from app.api.avatar_groups import service 
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.commons.api_models import ResponseEnvelope, status
from app.api.commons.auth.auth_bearer import JWTBearer

from app.api.commons.api_models import (
    GenericFilterParameters,
    OrderParameters,
    Pagination,
    PaginationParameters,
    ResponseEnvelope,
)
router = APIRouter()


@router.post(
    
    path = "",
    response_model=ResponseEnvelope,
    operation_id="createAvatarGroup",
    summary="Create AvatarGroup   Data.",
    status_code=status.HTTP_201_CREATED,
    
)
def create(
    db: Session = Depends(get_db),
    client:AvatarGroupBaseInsert=Body(...),
):
    AvatarGroup_response= service.create_avatar_groups(db,client)
    response_data = AvatarGroupResponse.from_orm(AvatarGroup_response)
    AvatarGroup_response = ResponseEnvelope(data=response_data)
    return AvatarGroup_response


@router.get(
    path="",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listAvatarGroup",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,

)
def get_all_avatar_groups(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_avatar_groups(
        session,
        pagination_params,
        order_params,
        filter_params,
    )

    response_data = [AvatarGroupResponse.from_orm(elem) for elem in response]

    response = ResponseEnvelope[List[AvatarGroupResponse]](
        data=response_data,
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
    operation_id="getAvatarGroupById",
    summary="Retrieve AvatarGroup data by id.",
    status_code=status.HTTP_200_OK,
)
def read_AvatarGroup_by_id(
    id: UUID,
    session: Session = Depends(get_db),
):
    """Endpoint for retrieving single Client info by id."""

    response = service.get_avatargroup_by_id(session, id)

    response_data = AvatarGroupResponse.from_orm(response)

    response = ResponseEnvelope[AvatarGroupResponse](data=response_data)

    return response

@router.delete(
    path="/{id}",
    operation_id="deleteAvatarGroupById",
    summary="Delete AvatarGroup Data by id.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_AvatarGroup__(
    id: int,
    session: Session = Depends(get_db),
):
    """Endpoint for deleting a single AvatarGroup data by id."""

    service.delete_avatar_group(session, id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    path="/{id}",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="putAvatarGroupById",
    summary="Update AvatarGroup  by id.",
    status_code=status.HTTP_200_OK,
)
def update_AvatarGroup__(
    id: int,
    AvatarGroup_update: AvatarGroupBaseInsert = Body(...),
    session: Session = Depends(get_db),
):
    """Endpoint for updating single AvatarGroup   Data by id."""

    response = service.update_avatar_group(
        session, id, AvatarGroup_update
    )
    response_data=AvatarGroupResponse.from_orm(response)
    response = ResponseEnvelope(data=response_data)
    return response
