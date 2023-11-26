from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from .utils import data_app
import pyexcel
import os

class MainPageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "mainapp/main_page.html", {})

    def post(self, request, *args, **kwargs):
        period = {"date1": request.POST.get("date1"), "date2": request.POST.get("date2")}
        tasks = data_app(period)
        headers = ['№ заявки', 'Статус', 'Название', 'Клиент', 'Создана', 'В работе', 'Осталось часов', 'Закрыта', 'Менеджер', 'Конструктор', 'номер заявки 1C', 'Метки', 'Фефко', 'Комментарий']
        data_2d_dict = {}
        data_2d_dict["Отчёт 1"] = [task for task in tasks]
        data_2d_dict["Отчёт 1"].insert(0, headers)

        '''Excel'''
        pyexcel.save_book_as(bookdict=data_2d_dict, dest_file_name = "report.xls")
        with open("report.xls", "rb") as fh:
            response = HttpResponse(fh.read(), content_type='application/vnd.ms-excel;charset=utf-8')
            response['Content-Disposition'] = "attachment; filename=report.xls"
            return response