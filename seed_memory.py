import uuid

from vanna_setup import agent
from vanna.core.user import UserResolver, User, RequestContext
from vanna.capabilities.agent_memory import ToolMemory
from vanna.core.tool import ToolContext
'''
examples = [
    "How many patients do we have?",
    "List all doctors",
    "Total revenue",
    "Patients by city",
    "Top 5 patients by spending"
]

for q in examples:
    try:
        print(f"Training on: {q}")
        agent.run(q)   # 👈 THIS is key
    except Exception as e:
        print("Handled:", e)

print("✅ Memory seeded via interactions!")'''


import asyncio
from vanna_setup import agent
from vanna.core.user import RequestContext

training_examples = [
    ToolMemory(
        question = "How many patients do we have?",
        tool_name ='run_sql',
        args = {
            'sql' : '''
    SELECT COUNT(*) AS total_patients FROM patients
                    '''
        }
    ),
    ToolMemory(
        question = 'List all patients with their city',
        tool_name ='run_sql',
        args = {
            'sql' : """ SELECT first_name,last_name , city FROM patients """
        }

    ),

    ToolMemory(
        question = 'patients from Delhi',
        tool_name = 'run_sql',
        args = {
            'sql' :   """ SELECT first_name , last_name FROM patients WHERE city = 'Delhi
 """      }
    ),

    ToolMemory(
        question = 'Count patient by gender',
        tool_name = 'run_sql',
        args = {
            'sql' : """ SELECT gender , COUNT(*) AS Total FROM patients GROUP BY gender
"""
        }
    ),

    ToolMemory(
        question = 'list all doctors and thier specifications',
        tool_name = 'run_sql',
        args = {
            'sql' : """ 
SELECT name , specialization FROM doctors
"""
        }
    ),

    ToolMemory(
        question = 'which doctors has most appoinments ? ',
        tool_name = 'run_sql',
        args = {
            'sql' : """ 
SELECT d.name , COUNT(*) as TOTAL_APPOINMENTS FROM appointments a
JOIN doctors d ON a.doctor_id = d.id GROUP BY d.name ORDER BY total_appoinments  DESC LIMIT 1
"""
        }
    ),

    ToolMemory(
        question = 'Show number of appoinmenrs per doctors ?',
        tool_name = 'run_sql',
        args = {
            'sql' : """ 
    SELECT d.name, COUNT(*) as TOTAL_APPOINMENTS FROM appoinments a  JOIN doctors d  ON  a.doctor_id = d.id
    GROUP BY  d.name
"""
        }
    ),

    ToolMemory(
        question = 'show all complete appoinments ',
        tool_name = 'run_sql',
        args = {
            'sql' : """ 
SELECT * FROM appointments WHERE status = 'Completed'
"""
        }
    ),

    ToolMemory(
        question = 'Count appoinments by status ',
        tool_name = 'run_sql',
        args = {
            'sql' : """
SELECT status , COUNT(*) FROM APPOINENTS GROUP BY status
"""
        }
    ),

     ToolMemory(
        question = 'Show appoinments from last month',
        tool_name = 'run_sql',
        args = {
            'sql' : """
SELECT * FROM APPOINENTS WHERE appoinment_date >= ('now','-1 month')
"""
        }
    ),

     ToolMemory(
        question = 'what is total revenue ?',
        tool_name = 'run_sql',
        args = {
            'sql' : """
SELECT SUM(total_amount as TOTAL REVENUE FROM invoices)
"""
        }
    ),

     ToolMemory(
        question = 'show unpaid invoices',
        tool_name = 'run_sql',
        args = {
            'sql' : """
SELECT * FROM invoices WHERE status != 'Paid'
"""
        }
    ),

     ToolMemory(
        question = 'Average treatment cost',
        tool_name = 'run_sql',
        args = {
            'sql' : """
SELECT AVG(cost) as AVG_COST FROM treatments
"""
        }
    ),

     ToolMemory(
        question = 'Appoinments in last 3 months',
        tool_name = 'run_sql',
        args = {
            'sql' : """
SELECT * FROM appointments WHERE appoinment_date >= ('now','-3 month')
"""
        }
    ),

    ToolMemory(
        question = 'Monthly appoinment trend',
        tool_name = 'run_sql',
        args = {
            'sql' : """ 
SELECT strftime('%Y-%m', appoinment_date) AS month, COUNT(*) AS total
FROM appointments GROUP BY  month ORDER BY month
"""
        }
    )




]

from vanna.core.user.models import User
your_user = User(id="admin", email="admin@example.com", group_memberships=["admin"])

from vanna.core.user import User
from vanna.core.tool import ToolContext
import uuid

async def seed_memory():
    for example in training_examples:
        await agent.agent_memory.save_tool_usage(
            question=example.question,
            tool_name=example.tool_name,
            args=example.args,
            context=ToolContext(
                user=User(id="admin", email="admin@test.com", group_memberships=["admin"]),
                conversation_id=str(uuid.uuid4()),
                request_id=str(uuid.uuid4()),
                agent_memory=agent.agent_memory
            ),
            success=True
        )

asyncio.run(seed_memory())