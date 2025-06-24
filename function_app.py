import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get the JSON string from the 'body' parameter
        body_str = req.params.get("body")
        logging.info(f"{body_str},{type(body_str)}")
        if not body_str:
            try:
                body_str = req.get_body().decode('utf-8')
            except Exception as e:
                logging.error("Could not read request body: " + str(e))
                return func.HttpResponse(
                    '{"Response": "Invalid Data"}',
                    mimetype="application/json",
                    status_code=400
                )
          
            logging.info(f"{body_str},{type(body_str)}")
        # Parse the string into a Python dictionary
        parsed_json = json.loads(body_str)

        # Extract the 'value' field which holds the employee list
        employee_list = parsed_json.get("value", [])

        # Validate each employee record
        for row in employee_list:
            emp_id = row.get("EmployeeID")
            name = row.get("Name")

            # Check if either field is null, empty, or whitespace
            if emp_id is None or str(emp_id).strip() == "" or \
               name is None or str(name).strip() == "":
                logging.info(f"Invalid row found: {row}")
                return func.HttpResponse(
                    '{"Response": "Invalid Data"}',
                    mimetype="application/json",
                    status_code=200
                )
            

        # If all rows are valid
        return func.HttpResponse(
            '{"Response": "Validation Passed"}',
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Validation error: {e}")
        return func.HttpResponse(
            '{"Response": "Invalid Data"}',
            mimetype="application/json",
            status_code=500
        )