from fastapi import FastAPI, HTTPException, APIRouter, Depends, Body, Response
from uuid import UUID
from typing import List
from app.api.avatar_groups.api_models import AvatarGroupResponse, AvatarGroupBaseInsert
from app.api.avatar_groups import service
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.commons.api_models import ResponseEnvelope, status

from app.api.commons.api_models import (
    GenericFilterParameters,
    OrderParameters,
    Pagination,
    PaginationParameters,
    ResponseEnvelope,
    ActionResponse,
)

router = APIRouter()


@router.post(
    path="",
    response_model=ActionResponse,
    operation_id="createAvatarGroup",
    summary="Create AvatarGroup Data.",
    status_code=status.HTTP_201_CREATED,
)
def create(
    db: Session = Depends(get_db),
    client: AvatarGroupBaseInsert = Body(...),
):
    AvatarGroup_response = service.create_avatar_groups(db, client)
    response_data = AvatarGroupResponse.from_orm(AvatarGroup_response)
    return ActionResponse(
        data=response_data.dict(),
        success=True,
        detail="Avatar Group created successfully"
    )


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
    response_data=[]
    for elem in response:
     response_elem=   AvatarGroupResponse.from_orm(elem)
     response_elem.no_of_avatars=len(service.get_avatarnumber_by_id(session,elem.id))
     response_data.append(response_elem)
    # response_data = [AvatarGroupResponse.from_orm(elem) for elem in response]

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
    id: int,
    session: Session = Depends(get_db),
):
    """Endpoint for retrieving single Client info by id."""

    response = service.get_avatargroup_by_id(session, id)

    response_data = AvatarGroupResponse.from_orm(response)

    response = ResponseEnvelope[AvatarGroupResponse](data=response_data)

    return response


@router.delete(
    path="/{id}",
    response_model=ActionResponse,
    response_model_exclude_none=True,
    operation_id="deleteAvatarGroupById",
    summary="Delete AvatarGroup data by id.",
    status_code=status.HTTP_200_OK,
)
def delete_AvatarGroup__(
    id: int,
    session: Session = Depends(get_db),
):
    """Endpoint for deleting a single AvatarGroup by id."""

    service.delete_avatar_group(session, id)
    return ActionResponse(
        data={},
        success=True,
        detail="Avatar Group deleted successfully"
    )



@router.put(
    path="/{id}",
    response_model=ActionResponse,
    response_model_exclude_none=True,
    operation_id="putAvatarGroupById",
    summary="Update AvatarGroup by id.",
    status_code=status.HTTP_200_OK,
)
def update_AvatarGroup__(
    id: int,
    AvatarGroup_update: AvatarGroupBaseInsert = Body(...),
    session: Session = Depends(get_db),
):
    """Endpoint for updating single AvatarGroup Data by id."""

    response = service.update_avatar_group(session, id, AvatarGroup_update)
    response_data = AvatarGroupResponse.from_orm(response)
    return ActionResponse(
        data=response_data.dict(),
        success=True,
        detail="Avatar Group updated successfully"
    )


@router.delete(
    path="/bulk/delete",
    response_model=ActionResponse,
    operation_id="bulkDeleteAvatarGroup",
    summary="Bulk delete AvatarGroup data.",
    status_code=status.HTTP_200_OK,
)
def bulk_delete_avatar_group(
    ids: List[int] = Body(...),
    session: Session = Depends(get_db),
):
    """Endpoint for bulk deleting AvatarGroup data."""

    service.bulk_delete_avatar_groups(session, ids)
    return ActionResponse(
        data={},
        success=True,
        detail="Avatar Group deleted successfully"
    )
