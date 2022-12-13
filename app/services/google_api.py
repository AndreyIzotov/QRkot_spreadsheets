from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
VERSION_SHEETS = 'v4'
VERSION_DRIVE = 'v3'
SHEETID = 0
ROWCOUNT = 100
COLUMNCOUNT = 11
TITLE = 'Лист1'
SHEETTYPE = 'GRID'
LOCATE = 'ru_RU'
TYPE = 'user'
ROLE = 'writer'
VALUEINPUTOPTION = 'USER_ENTERED'
MAJORDIMENSION = 'ROWS'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(
        'sheets',
        VERSION_SHEETS
    )
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': LOCATE
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': SHEETTYPE,
                    'sheetId': SHEETID,
                    'title': TITLE,
                    'gridProperties': {
                        'rowCount': ROWCOUNT,
                        'columnCount': COLUMNCOUNT
                    }
                }
            }
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': TYPE,
        'role': ROLE,
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover(
        'drive',
        VERSION_DRIVE
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover(
        'sheets',
        VERSION_SHEETS
    )
    table_values = [
        ['Отчет от', datetime.now().strftime(FORMAT)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']]
    for res in projects:
        new_row = [
            res['name'],
            res['delta'],
            res['description']
        ]
        table_values.append(new_row)
    update_body = {
        'majorDimension': MAJORDIMENSION,
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption=VALUEINPUTOPTION,
            json=update_body
        )
    )
