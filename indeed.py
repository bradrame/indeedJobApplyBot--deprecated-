import threading
import time
import tkinter as tk
#from tkinter import PhotoImage
#import pyautogui
from playwright.sync_api import sync_playwright
#from playwright.sync_api import expect


# application submission
# Tab: 'Upload or build a resume for this application | Indeed.com'
    # xpath for 'Continue': '//*[@id="ia-container"]/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[3]/div/button'
# Tab: 'Answer screener questions from the employer | Indeed.com'
    # xpath for question[0]: '//*[@id="q_0"]'
# Tab: 'Qualification check | Indeed.com'
    # xpath for 'Continue to application': '//*[@id="ia-container"]/div/div[1]/div/div/div/div[2]/div/div/main/div[3]/div/button[1]'
# Tab: 'Add relevant work experience information | Indeed.com'
    # xpath for 'Continue': '//*[@id="ia-container"]/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[3]/div/button'
    # xpath for popup2: '/html/body/div[6]/div[1]/div[2]/button[2]'

# Popup: Add some details..
    # xpath for 'Skip and review..': '/html/body/div[5]/div[1]/div[2]/button[2]'
# Tab: 'Review the contents of this job application | Indeed.com'
    # xpath for 'Submit your application': '//*[@id="ia-container"]/div/div/div/div/div[2]/div[2]/div/div/main/div[3]/div/button'
def submit_application():
    submission_tab = 'Review the contents of this job application | Indeed.com'
    resume_tab = 'Upload or build a resume for this application | Indeed.com'
    review_popup1 = '/html/body/div[5]/div[1]/div[2]/button[2]'
    questions_tab = 'Answer screener questions from the employer | Indeed.com'
    qualifications_tab = 'Qualification check | Indeed.com'
    addRelevant_tab = 'Add relevant work experience information | Indeed.com'
    review_popup2 = '/html/body/div[6]/div[1]/div[2]/button[2]'
    next_tab = browser.contexts[0].pages[1]
    time.sleep(2)
    while True:
        tab_name = next_tab.title()
        print(f'New tab: {tab_name}')
        if tab_name == submission_tab:
            next_tab.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            next_tab.click('//*[@id="ia-container"]/div/div/div/div/div[2]/div[2]/div/div/main/div[3]/div/button')
            next_tab.wait_for_timeout(3000)  # maybe unnecessary
            break
        elif tab_name == resume_tab:
            next_tab.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            next_tab.click('/html/body/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[3]/div/button[4]')
            next_tab.wait_for_timeout(3000)  # maybe unnecessary
            if next_tab.query_selector(review_popup1):
                next_tab.click(review_popup1)
        elif tab_name == questions_tab:
            # Create a question/answer mechanism
            break
        elif tab_name == qualifications_tab:
            next_tab.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            next_tab.click('//*[@id="ia-container"]/div/div[1]/div/div/div/div[2]/div/div/main/div[3]/div/button[1]')
        elif tab_name == addRelevant_tab:
            next_tab.click('//*[@id="ia-container"]/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[3]/div/button')
            next_tab.wait_for_timeout(3000)  # maybe unnecessary
            if next_tab.query_selector(review_popup2):
                next_tab.click(review_popup2)
        next_tab.wait_for_timeout(3000)
    next_tab.close()

# apply for jobs function
def apply_for_jobs():
    # intro before the big loop
    main_tab.wait_for_selector('//*[@id="text-input-what"]')
    main_tab.fill('//*[@id="text-input-what"]', job)
    main_tab.fill('//*[@id="text-input-where"]', city)
    main_tab.keyboard.press('Enter')
    xpath_wait_trigger = '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/button'
    main_tab.wait_for_selector(xpath_wait_trigger)
    if city is 'remote':
        pass
    else:
        main_tab.click('//*[contains(text(), "Location")]')
        main_tab.click('//*[@id="filter-loc-menu"]/li[1]')
    main_tab.wait_for_selector(xpath_wait_trigger)
    if salary is '':
        pass
    else:
        main_tab.click('//*[contains(text(), "Pay")]')
        main_tab.click(f'//*[@id="filter-salary-estimate-menu"]/li[{salary}]')
    main_tab.wait_for_selector(xpath_wait_trigger)
    if job_type is '':
        pass
    else:
        main_tab.click('//*[contains(text(), "Job type")]')
        main_tab.click(f'//*[contains(text(), "{job_type}")]')
    main_tab.wait_for_selector(xpath_wait_trigger)
    if experience is '':
        pass
    else:
        main_tab.click('//*[contains(text(), "Experience level")]')
        main_tab.click(f'//*[contains(text(), "{experience}")]')
    print(f'Main tab: ' + main_tab.title())
    # start the loop
    page_selector = 1
    apply_now = '//*[contains(text(), "Apply now")]'
    while applications > 0:
        print(f'\nJOBS PAGE {page_selector}')
        job_selector = 1
        # makes sure a job is available dynamically
        while True:
            job_card = main_tab.query_selector(f'//*[@id="mosaic-provider-jobcards"]/ul/li[{job_selector}]')
            if not job_card:
                print('\nAll job cards on this page have been viewed.')
                break
            else:
                print(f'\nWe are currently on job card {job_selector}')
                try:
                    main_tab.click(f'//*[@id="mosaic-provider-jobcards"]/ul/li[{job_selector}]')
                    main_tab.wait_for_selector(xpath_wait_trigger)
                    time.sleep(1)
                    if main_tab.is_visible(apply_now):
                        print('This card contains "Apply now"')
                        with browser.contexts[0].expect_event('page'):
                            main_tab.click(apply_now)
                        print(f'Tabs open: {len(browser.contexts[0].pages)}')
                        #time.sleep(3)
                        submit_application() # write close() in here
                        #time.sleep(3)
                    else:
                        print('This card doesn\'t contain "Apply now"')
                except:
                    print('This card doesn\'t contain "Apply now"')
                job_selector += 1
                # these job cards don't quite exist
                if job_selector in [6, 12, 18]:
                    job_selector += 1
                #time.sleep(3) # makes bot appear not suspicious
        page_selector += 1
        main_tab.click(f'//*[@id="jobsearch-JapanPage"]/div/div[5]/div[1]/nav/ul/li[*[contains(text(), "{str(page_selector)}")]]')

# login function
def login():
    print(f'Written preferences: {job} | {city} | {applications} applications')
    print(f'Selected preferences: {salary} | {job_type} | {experience}')
    def create_popup():
        def button_trigger():
            popup.destroy()
            button_clicked.set()
        popup = tk.Toplevel(root)
        popup.title('Popup')
        popup.attributes('-topmost', True)
        message_label = tk.Label(popup, text='Please log into your indeed account.\nOnce you have logged in click\n"Run bot" to start the process.')
        message_label.pack(padx=10, pady=10)
        button_run_bot = tk.Button(popup, text='Run bot', command=button_trigger)
        button_run_bot.pack(pady=10)
    # playwright setup
    def get_login_page():
        global p, browser, main_tab
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False, slow_mo=50)
            login_tab = browser.new_page()
            login_tab.set_default_timeout(5000)
            login_tab.goto('https://www.indeed.com')
            button_clicked.wait()
            login_tab.goto('https://www.indeed.com')
            # checks for accidental button press
            sign_in = '//*[@id="gnav-main-container"]/div/div/div[2]/div[2]/div[*[contains(text(), "Sign in")]]'
            if login_tab.is_visible(sign_in):
                browser.close()
                login()
            else:
                # CREATE HEAD/HEADLESS OPTIONS HERE
                if headless_var == False:
                    main_tab = login_tab
                    apply_for_jobs()
                else:
                    headless_browser = p.firefox.launch(headless=True, slow_mo=50)
                    browser = headless_browser
                    main_tab = browser.new_page()
                    main_tab.goto('https://www.indeed.com')
                    time.sleep(2)
                    login_tab.close()
                    main_tab.set_default_timeout(5000)
                    apply_for_jobs()
    create_popup()
    button_clicked = threading.Event()
    browser_thread = threading.Thread(target=get_login_page)
    browser_thread.start()

# menus setup
def indeed_menu():
    global root, question_index, job, city, applications, headless_var
    root = tk.Tk()
    root.title('Job Hunter [indeed.com]')
    root.geometry('450x550')
    #bg_image = PhotoImage(file='REPLACE.png')
    #bg_label = tk.Label(root, image=bg_image)
    #bg_label.place(relwidth=1, relheight=1)
    root.grid_rowconfigure(11, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    title_label = tk.Label(root, text='Welcome to Job Hunter [indeed.com]', font=('Helvetica Bold', 9, 'bold'))
    title_label.grid(row=0, column=1)
    # textbox menu
    questions = ['What position are you applying for?', 'Enter a city or type remote.', 'How many job applications do you\nwant me to apply for and submit?\n(10 to 20 is a good average)', 'Gotcha!\nNow it\'s time to adjust your job preferences.']
    question_index = 0
    job = '(job title)'
    city = '(job location)'
    applications = 0
    def rotate_question():
        global question_index
        question_index = (question_index + 1) % len(questions)
        question_label.config(text=questions[question_index])
        if question_index == 3:
            entry.destroy()
            written_label.destroy()
    def on_entry(event=None):
        global job, city, applications
        answer = entry.get()
        if answer.strip() != '':
            if question_index == 0:
                job = answer
                city = '(job location)'
                applications = 0
            elif question_index == 1:
                city = answer
                applications = 0
            elif question_index == 2:
                applications = int(answer)
            entry.delete(0, tk.END)
            written_label.config(text=f'Position: {job} | City: {city}')
            rotate_question()
    question_label = tk.Label(root, text=questions[question_index])
    question_label.grid(row=2, column=1)
    entry = tk.Entry(root, width=20)
    entry.grid(row=3, column=1)
    entry.bind('<Return>', on_entry)
    entry.focus()
    written_label = tk.Label(root, text=f'Position: {job} | City: {city}')
    written_label.grid(row=4, column=1)
    # dropdown menus
    def job_preferences():
        global salary, job_type, experience
        salary = ''
        job_type = ''
        experience = ''
        def update_preferences(*args):
            global salary, job_type, experience
            salary = selected_salary.get()
            job_type = selected_job_type.get()
            experience = selected_experience.get()
        # salary
        salary_label = tk.Label(root, text='Desired salary (optional)\n1 = low pay | 5 = high pay')
        salary_label.grid(row=7, column=1)
        salary_options = ['', '1', '2', '3', '4', '5']
        selected_salary = tk.StringVar(root)
        selected_salary.set(salary_options[0])
        salary = selected_salary.get()
        selected_salary.trace('w', update_preferences)
        salary_menu = tk.OptionMenu(root, selected_salary, *salary_options)
        salary_menu.grid(row=7, column=2)
        # job type
        job_type_label = tk.Label(root, text='Job type (optional)')
        job_type_label.grid(row=8, column=1)
        job_type_options = ['', 'Part-time', 'Full-time', 'Contract', 'Temporary', 'Internship']
        selected_job_type = tk.StringVar(root)
        selected_job_type.set(job_type_options[0])
        job_type = selected_job_type.get()
        selected_job_type.trace('w', update_preferences)
        job_type_menu = tk.OptionMenu(root, selected_job_type, *job_type_options)
        job_type_menu.grid(row=8, column=2)
        # experience level
        experience_label = tk.Label(root, text='Experience (optional)')
        experience_label.grid(row=10, column=1)
        experience_options = ['', 'No Experience Required', 'Entry Level', 'Mid Level', 'Senior Level']
        selected_experience = tk.StringVar(root)
        selected_experience.trace('w', update_preferences)
        experience_menu = tk.OptionMenu(root, selected_experience, *experience_options)
        experience_menu.grid(row=10, column=2)
    disclaimer_label = tk.Label(root, text='')
    disclaimer_label.grid(row=11, column=1)
    # additional buttons menu
    def toggle_headless():
        global headless_var
        headless_var = not headless_var
        print(f'Headless mode: {headless_var}')
    headless_var = False
    headless_checkbox = tk.Checkbutton(root, text='Invisible Mode', font=('Helvetica', 8), command=toggle_headless) # state=tk.DISABLED
    headless_checkbox.grid(row=13, column=0, pady=5)
    login_button = tk.Button(root, text='Login', font=('Helvetica', 15, 'bold'), width=20, state=tk.DISABLED, command=login)
    login_button.grid(row=12, column=1)
    quit_app_button = tk.Button(root, text='Quit App', font=('Helvetica', 9, 'bold'), command=root.destroy)
    quit_app_button.grid(row=12, column=0, padx=10)
    # checking questions index for new question
    def check_question_index():
        if question_index == 3:
            job_preferences()
            disclaimer_label.config(text='Once your preferences are complete\nclick "Login" to navigate to the\nindeed login page. This is where\nyou will log into your account and\nbe prompted to activate the bot.')
            login_button.config(state=tk.NORMAL)
        if question_index < len(questions) - 1:
            root.after(100, check_question_index)
    check_question_index()

    root.mainloop()


if __name__ == "__main__":
    indeed_menu()