import xlwt
from django.db.models.functions import TruncWeek
from django.http import HttpResponse
from django.db.models import Count, Sum
from django.utils import timezone

from robots.models import Robot


def export_to_excel(request):
    # Определим начало и конец текущей недели
    today = timezone.now()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)

    # Выборка данных для агрегации
    aggregated_data = (
        Robot.objects
        .filter(created__gte=start_of_week, created__lte=end_of_week)  # Фильтр по дате
        .annotate(week=TruncWeek('created'))
        .values('model', 'version', 'week')
        .annotate(total_count=Count('id'))
    )

    # Создание новой книги Excel
    wb = xlwt.Workbook(encoding='utf-8')

    current_model = None

    for entry in aggregated_data:
        model = entry['model']
        version = entry['version']
        total_count = entry['total_count']
        week = entry['week']

        if current_model != model:
            # Создание нового листа Excel для новой модели
            ws = wb.add_sheet(f'{model}')

            row_num = 0
            columns = ["Модель", "Версия", "Количество за неделю"]

            for col_num, column_title in enumerate(columns):
                ws.write(row_num, col_num, column_title)

            current_model = model

        row_num += 1
        row = [model, version, total_count]

        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="robot_data.xls"'
    wb.save(response)

    return response