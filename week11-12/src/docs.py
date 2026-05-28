def swagger_html():

    return """
<!DOCTYPE html>
<html>

<head>
<link rel="stylesheet"
href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">

<title>TaskFlow Swagger</title>
</head>

<body>

<div id="swagger-ui"></div>

<script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>

<script>

window.onload = () => {

SwaggerUIBundle({
    url: '/openapi.json',
    dom_id: '#swagger-ui'
});

};

</script>

</body>
</html>
"""