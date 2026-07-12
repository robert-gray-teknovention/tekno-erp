from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from employee.models import TimesheetUser
from organizations.models import Organization
from timesheets.models import TimesheetEntry, TimesheetPeriod
from .models import WorkEntry, WorkOrder


class TimesheetEntryPromotionViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.ts_user = TimesheetUser.objects.create(user=self.user)
        self.organization = Organization.objects.create(
            name='Test Org',
            street1='123 Main',
            city='Testville',
            zip='12345',
            state='TX',
            phone='555-0100',
            mailer_email='test@example.com',
        )
        self.period = TimesheetPeriod.objects.create(
            org=self.organization,
            date_start='2026-07-01T00:00:00Z',
            date_end='2026-07-15T23:59:59Z',
        )
        self.timesheet_entry = TimesheetEntry.objects.create(
            user=self.ts_user,
            date_time_in='2026-07-10T08:00:00Z',
            date_time_out='2026-07-10T12:00:00Z',
            duration=4.0,
            period=self.period,
            notes='Promote me',
        )
        self.work_order = WorkOrder.objects.create(request='Need this promoted entry')

    def test_promotion_creates_workentry_and_redirects(self):
        self.client.force_login(self.user)
        url = reverse('workorders:timesheetentry-promote', kwargs={'pk': self.timesheet_entry.pk})

        response = self.client.post(url, {'work_order': self.work_order.pk})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(WorkEntry.objects.filter(timesheetentry_ptr=self.timesheet_entry).exists())
        work_entry = WorkEntry.objects.get(timesheetentry_ptr=self.timesheet_entry)
        self.assertEqual(work_entry.work_order, self.work_order)
        self.assertEqual(work_entry.notes, 'Promote me')
