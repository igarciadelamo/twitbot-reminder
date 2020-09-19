import unittest

from twitbotreminder.model import ReminderList


class ReminderListCase(unittest.TestCase):
    def test_create_list(self):
        reminder_list = create_reminder_list(7)
        self.assertEqual(7, len(reminder_list.list))

    def test_create_empty_list(self):
        reminder_list = create_reminder_list(0)
        self.assertEqual(0, len(reminder_list.list))

    def test_search_by_date_with_results(self):
        reminder_list = create_reminder_list(3)
        filtered = reminder_list.search_by_date(1, 3)
        self.assertEqual(1, len(list(filtered)))

    def test_search_by_date_with_no_results(self):
        reminder_list = create_reminder_list(3)
        filtered = reminder_list.search_by_date(19, 3)
        self.assertEqual(0, len(list(filtered)))


def create_reminder_list(num_elements):
    reminders = create_list(num_elements)
    return ReminderList(reminders)


def create_list(num_elements):
    list = []
    for index in range(0, num_elements):
        data = {"month": 3, "dayOfMonth": index, "text": "reminder num_" + str(index)}
        list.append(data)
    return list


def main():
    unittest.main()


if __name__ == "__main__":
    main()
