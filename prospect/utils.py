from calendar import HTMLCalendar, monthrange
from datetime import datetime, timedelta
from prospect import models as prospectModels
import calendar
from django.utils import timezone
from django.db.models import Max

from tabernacle_customer_success import constants
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, firstweekday=6):
        self.year = year
        self.month = month
        self.firstweekday = firstweekday
        super(Calendar, self).__init__(firstweekday=self.firstweekday)

    # formats a day
    # filter events by day
    def formatday(self, day, prospects):
        prospects_per_day = prospects.filter(date__day=day, date__month=self.month, date__year=self.year)
        d = []
        for prospect in prospects_per_day:
            status_history = prospectModels.StatusHistory.objects.filter(prospect_id=prospect.prospect.uuid).order_by('-created_at')
            prospect.status_history = status_history.first()
            if prospect.status_history.status == constants.TRIAL:
                prospect.expiry_date = prospect.status_history.date + timedelta(days=14)
                prospect.expiry_days = (prospect.expiry_date - timezone.now()).days
            d.append(prospect) 
        return d
    
    def format_day_trailing_months(self, month_day, month, year, prospects):
        # events_per_day = events.filter(start_date__day=month_day, start_date__month=month, start_date__year=year)
        # events_per_day = events.filter(None)
        d = []
        # for event in events_per_day:
        #     d.append(event) 
        d.append('') 

        return d

    # formats a week header
    def formatweekheader(self):
        # Get the weekday names starting from the first weekday
        weekday_names = calendar.day_name[self.firstweekday:] + calendar.day_name[:self.firstweekday]
        truncated_names = [day[:3] for day in weekday_names]
        return truncated_names

    # formats a week
    def formatweek(self, theweek, events):
        week = []
        for d, weekday in theweek:
            week.append(self.formatday(d, events))
        return week

    # formats a month
    # filter events by year and month
    def formatmonth(self, withyear=True):
        today = datetime.today()


        prospects__ids = prospectModels.Profile.objects.filter(status=constants.MEETING_SCHEDULED).distinct('uuid').values_list('uuid', flat=True)

        # for prospect in prospects:
        #     prospect.status = prospectModels.StatusHistory.objects.filter(prospect_id=prospect.uuid, date__month=today.month,
        #     date__year=today.year).order_by('-created_at').first()


        status_history = prospectModels.StatusHistory.objects.filter(
            date__month=today.month,
            date__year=today.year,
            prospect_id__in = prospects__ids,
            status=constants.MEETING_SCHEDULED
        ).order_by('prospect', 'created_at')

        latest_records = status_history.values('prospect').annotate(
            latest_date=Max('created_at')
        )

        prospects = prospectModels.StatusHistory.objects.filter(
            date__month=today.month,
            date__year=today.year,
            status=constants.MEETING_SCHEDULED,
            prospect__in=latest_records.values_list('prospect', flat=True),
            created_at__in=latest_records.values_list('latest_date', flat=True)
        )
        
        # prospects = prospectModels.StatusHistory.objects.filter(status=constants.MEETING_SCHEDULED)
        cal_data = []

        for week_start, week in zip(self.monthdays2calendar(self.year, self.month), self.monthdays2calendar(self.year, self.month)):
            week_data = []
            prev_month_day = None
            next_month_day = 1

            for day, weekday in week:
                if day == 0:
                    # Trailing days of the previous month
                    if week == self.monthdays2calendar(self.year, self.month)[0]:
                        # Simply add the days of the previous month till day != 0
                        if prev_month_day:
                            prev_month_day += 1
                        else:
                            # Find the last week of the previous month
                            prev_month = self.month - 1 if self.month > 1 else 12 
                            prev_year = self.year if self.month > 1 else self.year - 1
                            last_week_of_prev_month = self.monthdays2calendar(prev_year, prev_month)[-1]
                            # This will return the date of (Sunday) from the last week of the previous month.
                            prev_month_day = last_week_of_prev_month[0][0]
                        prospects_data = self.format_day_trailing_months(prev_month_day, prev_month, prev_year, prospects)
                        week_data.append({
                                'day': self._format_combined_date(prev_month_day, prev_month, prev_year),
                                'prospects': prospects_data
                            })
                    # Trailing days of the next month
                    elif week == self.monthdays2calendar(self.year, self.month)[-1]:
                        # Adjust for December to January transition
                        next_month = 1 if self.month == 12 else self.month + 1
                        next_year = self.year + 1 if self.month == 12 else self.year
                        prospects_data = self.format_day_trailing_months(next_month_day, next_month, next_year, prospects)
                        week_data.append({
                                'day': self._format_combined_date(next_month_day, next_month, next_year),
                                'prospects': prospects_data
                            })
                        next_month_day += 1
                else:
                    prospects_data = self.formatday(day, prospects)
                    week_data.append({
                                'day': self._format_combined_date(day, self.month, self.year),
                                'prospects': prospects_data
                            })
            cal_data.append(week_data)
        return cal_data

    def _format_combined_date(self, day, month, year):
        combined_date = datetime(year, month, day)
        return combined_date