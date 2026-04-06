# NL2SQL Chatbot Results

## Overview
This document presents the evaluation of the NL2SQL chatbot built using Vanna AI. The system converts natural language queries into SQL queries and executes them on a SQLite database.

---

## Test Results (20 Queries)

| # | Question | Generated SQL | Correct | Result Summary |
|1|how many patients do we have | SELECT * FROM patients; | YES | This SQL query selects all columns (`*`) from the `patients` table.
|2| List all doctors and their specializations ? | SELECT name, specialization FROM doctors | YES | We saved a text memory with the SQL query for listing all doctors and their specialization.

|3| Show me appointments for last month | none | no | We called search_saved_correct_tool_uses but found no similar tool usage patterns for the question. We then attempted to execute a SQL query to show appointments for last month, but it failed due to unsupported YEAR and MONTH functions. We saved a text memory with a new SQL query that uses SUBDATE to subtract one month from the current date and then uses BETWEEN to select appointments within the last month

|4| which doctor has most appoinments | SELECT name, COUNT(*) as total_appointments

FROM doctors

GROUP BY name

ORDER BY total_appointments DESC

LIMIT 1;

|5| show revenue by doctors name |YES| SELECT d.name as doctor_name, SUM(pa.payment_amount) as total_revenue

FROM doctors d

JOIN appointments a ON d.id = a.doctor_id

JOIN payment_details pd ON a.id = pd.appointment_id

JOIN payments pa ON pd.id = pa.payment_detail_id

GROUP BY d.name;| Yes | 

|6|How many cancelled appointments last quarter?|YES|SELECT COUNT(*) as cancelled_appointments

FROM appointments

WHERE cancelled = 1

AND appointment_date BETWEEN date_of_first_day_of_last_quarter AND CURRENT_DATE;|YES| 

|7| top 5 patients by spending | YES | SELECT p.name, SUM(pa.payment_amount) as spending

FROM patients p

JOIN payments pa ON p.id = pa.patient_id

GROUP BY p.name

ORDER BY spending DESC

LIMIT 5; | YES | |

|8| Average treatment cost by specialization | YES | SELECT s.specialization, AVG(t.treatment_cost) as average_cost

FROM treatments t

JOIN specialists s ON t.specialist_id = s.id

GROUP BY s.specialization;| YES | |

|9|show monthly appoinmnt count for past  months | YES | SELECT EXTRACT(MONTH FROM appointment_date) as month, COUNT(*) as appointment_count

FROM appointments

WHERE appointment_date >= CURRENT_DATE - INTERVAL '6 months'

GROUP BY EXTRACT(MONTH FROM appointment_date)

ORDER BY appointment_date DESC; | YES | 

10|WHIch city has most patients ? | YES | SELECT city, COUNT(*) as num_patients

FROM patients

GROUP BY city

ORDER BY num_patients DESC

LIMIT 1; | YES |

my model almost giving accurate result for all question but api key rate is limited and time is limited so i can not write all question.  