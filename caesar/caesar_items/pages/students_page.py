import os
from selenium.webdriver.support.ui import WebDriverWait
from caesar_items.pages.base_page import BasePage
from caesar_items.locators.locators import StudentsListLocators, \
    StudentLocators
from resource.error_handler import logger_exception


# the number of seconds the driver will wait until element become enabled
seconds = 30


class Student(object):

    def __init__(self, first_name, last_name, incoming_mark,
                 entry_mark, english_level, approved_by,
                 approved_by_custom=None):
        """This Object describes the Student"""
        self.first_name = first_name
        self.last_name = last_name
        self.incoming_mark = incoming_mark
        self.entry_mark = entry_mark
        self.english_level = english_level
        self.approved_by = approved_by
        self.approved_by_custom = approved_by_custom


class StudentData(object):

    def __init__(self, driver):
        """This Page Object describes the fields and buttons of the modal
        window that you can use for input student's data."""
        self.driver = driver
        self.first_name = WebDriverWait(self.driver, seconds).\
            until(lambda chrome: self.driver.
                  find_element(*StudentLocators.FIRST_NAME_TEXT_FIELD))
        self.last_name = \
            self.driver.find_element(*StudentLocators.LAST_NAME_TEXT_FIELD)
        self.entry_score = \
            self.driver.find_element(*StudentLocators.STUDENT_ENTRY_SCORE)
        self.mark_incoming_test = \
            self.driver.find_element(*StudentLocators.
                                     STUDENT_MARK_INCOMING_TEST)
        self.add_cv_file_button = \
            self.driver.find_element(*StudentLocators.ADD_CV_BUTTON)
        self.add_photo_file_button =\
            self.driver.find_element(*StudentLocators.ADD_PHOTO_BUTTON)
        self.save_data_changes_button = WebDriverWait(self.driver, seconds).\
            until(lambda chrome: self.driver.
                  find_element(*StudentLocators.SAVE_CHANGES_BUTTON))

    @logger_exception
    def click_save_data_changes_button(self):
        """ Click button to save changes in student data."""
        self.save_data_changes_button.click()
        return StudentsList(self.driver)

    @logger_exception
    def enter_student_first_name(self, first_name):
        """ Enter student first name in window 'student data'."""
        self.first_name.clear()
        self.first_name.send_keys(first_name)

    @logger_exception
    def enter_student_last_name(self, last_name):
        """ Enter student last name in window 'student data'."""
        self.last_name.clear()
        self.last_name.send_keys(last_name)

    @logger_exception
    def select_english_level(self, english_level):
        """ Enter student's english level in
        window 'student data'."""
        self.driver.find_element(*StudentLocators.
                                 OPEN_ENGLISH_LEVELS_LIST).click()
        english_levels_list = \
            self.driver.find_elements(*StudentLocators.
                                      ENGLISH_LEVELS_LIST)
        for level in english_levels_list:
            if level.text == english_level:
                level.click()

    @logger_exception
    def enter_student_mark_incoming_test(self, incoming_mark):
        """ Enter student's mark of incoming test in
        window 'student data'."""
        self.mark_incoming_test.clear()
        self.mark_incoming_test.send_keys(incoming_mark)

    @logger_exception
    def enter_student_entry_mark(self, entry_mark):
        """ Enter student's entry mark in
        window 'student data'."""
        self.entry_score.clear()
        self.entry_score.send_keys(entry_mark)

    @logger_exception
    def select_who_approved(self, approved_by):
        """ Enter who approved student in
        window 'student data'."""
        self.driver.find_element(*StudentLocators.
                                 OPEN_LIST_APPROVED_BY).click()
        list_who_approved = \
            self.driver.find_elements(*StudentLocators.
                                      LIST_WHO_APPROVED)
        for person in list_who_approved:
            if person.text == approved_by:
                person.click()

    @logger_exception
    def enter_name_approved_by_custom(self, student):
        """ Enter approved by custom(name) student in
        window 'student data'."""
        self.driver.find_element(*StudentLocators.
                                 APPROVED_BY_CUSTOM).\
            send_keys(student.approved_by_custom)
        return self

    @logger_exception
    def enter_student_data(self, student):
        """ Common function for enter all necessary fields for
        student's data."""
        self.enter_student_first_name(student.first_name)
        self.enter_student_last_name(student.last_name)
        self.select_english_level(student.english_level)
        self.enter_student_mark_incoming_test(student.incoming_mark)
        self.enter_student_entry_mark(student.entry_mark)
        self.select_who_approved(student.approved_by)
        return self

    @logger_exception
    def add_cv(self, path_file_cv):
        """ Input cv file for student data."""
        self.add_cv_file_button.click()
        self.driver.find_element(*StudentLocators.
                                 INPUT_PATH_CV_FILE). \
            send_keys(os.path.abspath(path_file_cv))
        return self

    @logger_exception
    def get_name_cv_file(self):
        """ Return name of last cv file, which is input in student data."""
        cv_names_list = []
        for cv in self.driver.find_elements(*StudentLocators.FILE_CV):
            cv_names_list.append(cv.find_element(*StudentLocators.
                                                 FILE_NAME_CV).text)
        return cv_names_list[-1]

    @logger_exception
    def add_photo(self, path_file_photo):
        """ Input photo file for student data."""
        self.add_photo_file_button.click()
        self.driver.find_element(*StudentLocators.
                                 INPUT_PATH_PHOTO_FILE). \
            send_keys(os.path.abspath(path_file_photo))
        return self

    @logger_exception
    def get_name_photo_file(self):
        """ Return name of last photo file, which is input in student data."""
        return self.driver.find_elements(*StudentLocators.
                                         FILE_NAME_PHOTO)[-1].text

    @logger_exception
    def warnings_text_for_adding_student_with_empty_fields(self):
        """ Return warnings text after adding student with empty fields."""
        warnings_text = []
        warnings = WebDriverWait(self.driver, seconds). \
            until(lambda chrome: self.driver.
                  find_elements(*StudentLocators.
                                WARNINGS_ADD_EMPTY_STUDENT_DATA))
        for message in warnings:
            warnings_text.append(message.text)
        return warnings_text


class StudentsList(object):

    def __init__(self, driver):
        """This Page Object describes buttons of the modal
        window that you can use for adding, removal and
        editing student's data."""
        self.driver = driver
        self.add_new_student_button = \
            self.driver.find_element(*StudentsListLocators.
                                     ADD_NEW_STUDENT_BUTTON)
        self.edit_student_button = \
            self.driver.find_element(*StudentsListLocators.
                                     EDIT_STUDENT_BUTTON)
        self.delete_first_student_button = \
            self.driver.find_element(*StudentsListLocators.
                                     DELETE_STUDENT_BUTTON)
        self.exit_students_list_editor_button = \
            self.driver.find_element(*StudentsListLocators.
                                     EXIT_EDIT_STUDENTS_LIST_BUTTON)

    @logger_exception
    def click_delete_first_student_button(self):
        """ Click on button for deleting first student
        from the student's list."""
        self.delete_first_student_button.click()
        WebDriverWait(self.driver, seconds). \
            until(lambda chrome: self.driver.
                  find_element(*StudentsListLocators.
                               CONFIRM_DELETING_BUTTON)).click()
        return StudentsList(self.driver)

    @logger_exception
    def click_add_new_student_button(self):
        """ Click on button for opening window for adding
        new student's data."""
        self.add_new_student_button.click()
        return StudentData(self.driver)

    @logger_exception
    def click_edit_student_button(self):
        """ Click on button for opening window for editing
        student's data."""
        self.edit_student_button.click()
        return StudentData(self.driver)

    @logger_exception
    def click_exit_students_list_editor_button(self):
        """ Click on button for exit from the student's list editor."""
        self.exit_students_list_editor_button.click()
        return StudentsPage(self.driver)


class StudentsPage(BasePage):

    def __init__(self, driver):
        """This Page Object describes buttons of the
        window that you can use for editing student's list and
        sorting student's list by name."""
        super().__init__(driver)

    @logger_exception
    def students_table(self):
        """ Return list of students data."""
        students_data = []
        list_rows = WebDriverWait(self.driver, seconds). \
            until(lambda chrome: self.driver.
                  find_elements(*StudentsListLocators.
                                STUDENTS_LISTS_ROWS))
        for rows in list_rows:
            students_data.append(rows.text)
        return students_data

    @logger_exception
    def click_edit_students_list_button(self):
        """ Click on button for entering student's list editor."""
        WebDriverWait(self.driver, seconds). \
            until(lambda chrome: self.driver.
                  find_element(*StudentsListLocators.
                               EDIT_STUDENTS_LIST_BUTTON)).click()
        return StudentsList(self.driver)

    @logger_exception
    def click_students_from_group_button(self):
        """ Click on button students after selecting group."""
        WebDriverWait(self.driver, seconds). \
            until(lambda chrome: self.driver.
                  find_element(*StudentsListLocators.
                               STUDENTS_IN_STUDENTS_LIST_BUTTON)).click()
        return StudentsList(self.driver)

    @logger_exception
    def click_students_list_sort_by_name_button(self):
        """ Click on button for sorting student's list by name."""
        self.driver.find_element(*StudentsListLocators.
                                 SORT_LIST_BY_NAME_BUTTON).click()
        return self

@logger_exception
def data_student_for_check(student):
    """ Return student's data after adding student."""
    if student.approved_by_custom is None:
        data_student = [student.last_name, student.first_name,
                        student.english_level, student.incoming_mark,
                        student.entry_mark, student.approved_by]
        data_student = ' '.join(data_student)
        return data_student
    elif student.approved_by_custom is not None:
        data_student = [student.last_name, student.first_name,
                        student.english_level, student.incoming_mark,
                        student.entry_mark, student.approved_by_custom]
        data_student = ' '.join(data_student)
        return data_student

@logger_exception
def remove_none_from_list(students_list):
    """ Return students list without None."""
    return list(filter(None, students_list))


def sorted_students_list(students_list):
    """ Return sorted students list."""
    remove_none_from_list(students_list)
    return sorted(students_list)
