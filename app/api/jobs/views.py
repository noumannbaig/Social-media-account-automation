from fastapi import FastAPI, HTTPException, APIRouter, Depends, Body, Query, Response
from uuid import UUID
from typing import List

from sqlalchemy.orm import Session
from app.api.jobs.api_models import JobResponse, SchedulerResponse, SchedulerTaskResponse
from app.database.session import get_db
from app.api.commons.api_models import ResponseEnvelope, status
from app.api.jobs import service
from app.api.commons.api_models import (
    GenericFilterParameters,
    OrderParameters,
    Pagination,
    PaginationParameters,
    ResponseEnvelope,
)

router = APIRouter()


@router.get(
    path="",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listSchedulers",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_schedulers(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_all_schedulers(
        session,
        pagination_params,
        order_params,
        filter_params,
    )

    #response_data = [SchedulerResponse.from_orm(elem) for elem in response]
    response_data=[]
    for elem in response:
        
        scheduler_response = SchedulerResponse.from_orm(elem)
        if scheduler_response.start_time is None:
            scheduler_response.start_time=None
        if scheduler_response.end_time is None:
            scheduler_response.end_time=None
        scheduler_response.job = elem.jobs.code
        scheduler_response.scheduler_status=elem.status.code
        response_data.append(scheduler_response)
    response = ResponseEnvelope[List[SchedulerResponse]](
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
    operation_id="getAvatarById",
    summary="Retrieve Avatar data by id.",
    status_code=status.HTTP_200_OK,
)
def read_SchedulerTask_by_scheduler_id(
    id: int,
    session: Session = Depends(get_db),
):
    """Endpoint for retrieving single Client info by id."""

    response = service.get_schedulerTask_by_Schedulerid(session, id)

    response_data=[]
    for elem in response:
        
        scheduler_response = SchedulerTaskResponse.from_orm(elem)
        if scheduler_response.start_time is None:
            scheduler_response.start_time=None
        if scheduler_response.end_time is None:
            scheduler_response.end_time=None
        scheduler_response.task_id=elem.task_id
        scheduler_response.task_code=elem.task.code
        scheduler_response.scheduler_task_status_id=elem.status.id
        scheduler_response.status_code=elem.status.code
        response_data.append(scheduler_response)
    response = ResponseEnvelope[List[SchedulerTaskResponse]](
        data=response_data)

    return response