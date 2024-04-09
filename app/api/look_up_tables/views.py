from fastapi import FastAPI, HTTPException, APIRouter, Depends, Body, Response
from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from app.api.look_up_tables import service
from app.api.look_up_tables.api_models import CountriesBase, GenderBase, LanguageBase, NationalityBase, PlatformsBase, ProvidersBase
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



@router.get(
    path="/platforms",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="lisPlatforms",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_platforms(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_platforms(
        session,
        pagination_params,
        order_params,
        filter_params,
    )

    response_data = [PlatformsBase.from_orm(elem) for elem in response]

    response = ResponseEnvelope[List[PlatformsBase]](
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
    path="/providers",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listproviders",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_providers(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_providers(
        session,
        pagination_params,
        order_params,
        filter_params,
    )

    response_data = [ProvidersBase.from_orm(elem) for elem in response]

    response = ResponseEnvelope[List[ProvidersBase]](
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
    path="/countries",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listcountries",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_countries(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_countries(
        session,
        pagination_params,
        order_params,
        filter_params,
    )

    response_data = [CountriesBase.from_orm(elem) for elem in response]

    response = ResponseEnvelope[List[CountriesBase]](
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
    path="/nationalities",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listnationalities",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_countries(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_nationalities(
        session,
        pagination_params,
        order_params,
        filter_params,
    )

    response_data = [NationalityBase.from_orm(elem) for elem in response]

    response = ResponseEnvelope[List[NationalityBase]](
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
    path="/gender",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listgender",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_genders(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_genders(
        session,
        pagination_params,
        order_params,
        filter_params,
    )

    response_data = [GenderBase.from_orm(elem) for elem in response]

    response = ResponseEnvelope[List[GenderBase]](
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
    path="/languages",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listlanguages",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_languages(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_languages(
        session,
        pagination_params,
        order_params,
        filter_params,
    )

    response_data = [LanguageBase.from_orm(elem) for elem in response]

    response = ResponseEnvelope[List[LanguageBase]](
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
    path="/relationship-status",
    response_model=ResponseEnvelope,
    response_model_exclude_none=True,
    operation_id="listrelationship-status",
    summary="Retrieve list of  Data.",
    status_code=status.HTTP_200_OK,
)
def get_all_languages(
    session: Session = Depends(get_db),
    pagination_params: PaginationParameters = Depends(PaginationParameters),
    order_params: OrderParameters = Depends(OrderParameters),
    filter_params: GenericFilterParameters = Depends(GenericFilterParameters),
):
    """Endpoint for retrieving all AvatarGroup entities."""

    response, total_pages, total_elements = service.get_relationship_statuses(
        session,
        pagination_params,
        order_params,
        filter_params,
    )

    response_data = [LanguageBase.from_orm(elem) for elem in response]

    response = ResponseEnvelope[List[LanguageBase]](
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