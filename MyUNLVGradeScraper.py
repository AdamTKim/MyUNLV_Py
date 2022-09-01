#Import libraries
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

#Global variables
GRADE_FLAGS = []
LOGIN_URL = "https://my.unlv.nevada.edu/psp/lvporprd/?cmd=login&languageCd=ENG&"
GRADES_URL = "https://my.unlv.nevada.edu/psp/lvporprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?PORTALPARAM_PTCNAV=HC_SSR_SSENRL_GRADE_GBL&EOPP.SCNode=SA&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=CO_EMPLOYEE_SELF_SERVICE&EOPP.SCLabel=Enrollment&EOPP.SCFName=HCCC_ENROLLMENT&EOPP.SCSecondary=true&EOPP.SCPTfname=HCCC_ENROLLMENT&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ENROLLMENT.HC_SSR_SSENRL_GRADE_GBL&IsFolder=false"
 
def main():

        #Prompt for user inputs
        myunlv_username = input("Enter your MyUNLV username: ")
        myunlv_password = input("Enter your MyUNLV password: ")
        email_to = input("Enter the email address to send your grades to: ")
        num_classes = int(input("Enter the number of classes you are taking THIS semester: "))
        next_semester = input("Enter the NEXT semester in the format YEAR SEASON (i.e. 2021 Spring): ")

        #Setup GRADE_FLAGS
        for i in range(num_classes):
            GRADE_FLAGS.append(True)

        #Set up options for Chrome Webdriver
        chromeoptions = webdriver.ChromeOptions()
        chromeoptions.add_argument('--disable-extensions')
        chromeoptions.add_argument('--headless')
        chromeoptions.add_argument('--disable-gpu')
        chromeoptions.add_argument('--no-sandbox')
        chromeoptions.add_argument('--log-level=3')
        chromeoptions.add_argument('--ignore-certificate-errors')
        chromeoptions.add_argument('--ignore-ssl-errors')

        #Check for sent grades and loop until all have been sent
        while True in GRADE_FLAGS:

            #Set up webdriver, log into MyUNLV, and navigate to the grades webpage
            driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(), options = chromeoptions)
            driver.get(LOGIN_URL)
            driver.find_element(By.ID, "userid").send_keys(myunlv_username)
            driver.find_element(By.ID, "pwd").send_keys(myunlv_password)
            driver.find_element(By.XPATH, "/html/body/div/form/div/div[1]/div[6]/input").click()
            driver.get(GRADES_URL)
            time.sleep(2)

            #Set up email server
            server = smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465)
            server.login("Adamkim13", "ypxmeesgbfocodar")
                
            #Code to check which semester grades need to be pulled when the next semester is added
            driver.switch_to.frame("ptifrmtgtframe")
                
            if ((driver.find_element(By.ID, "TERM_CAR$0")).text).upper == next_semester.upper:
                    driver.find_element(By.XPATH, "/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[4]/td[2]/div/table/tbody/tr[2]/td/table/tbody/tr[3]/td[1]/div/input").click()
            else:
                    driver.find_element(By.XPATH, "/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[4]/td[2]/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/div/input").click()

            driver.find_element(By.XPATH, "/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/a/span/input").click()
            time.sleep(2)

            #Pull the class names and grades then save them to local variables
            driver.switch_to.default_content()
            driver.switch_to.frame("ptifrmtgtframe")
            time.sleep(2)

            #Loop through all classes
            for x in range(num_classes):

                    class_name = (driver.find_element(By.ID, "CLS_LINK$" + str(x))).text
                    grade = (driver.find_element(By.ID, "STDNT_ENRL_SSV1_CRSE_GRADE_OFF$" + str(x))).text
        
                    #Send email
                    if grade != " " and GRADE_FLAGS[x]:
                            msg = MIMEMultipart()
                            msg["Subject"] = class_name + " FINAL GRADE: " + grade
                            server.sendmail("Adamkim13@yahoo.com", email_to, msg.as_string())
                            print("SENDING " + class_name + " GRADE")
                            GRADE_FLAGS[x] = False

            #Print status message and quit both the Chromedriver and the SMTP server. Sleep for 5 minutes
            print("Run at ", datetime.now())
            driver.quit()
            server.quit()
            time.sleep(300) 

        #Once done sending all grades exit program
        sys.exit()
        
if __name__ == '__main__':
    main()
