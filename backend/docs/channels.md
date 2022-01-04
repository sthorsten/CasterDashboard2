# Django Channels Setup

## Overview

Django Channels is used to establish and manage realtime websocket connections with the frontend.
This provides fast data fetching as well as the ability to push data to the client when changes such as updating match and map data occur.

Since arbitrary (binary and text) data can be transferred via the websocket protocol, the following custom protocol will be used:

- All data are being sent in the JSON format. Encoding and decoding has to be handled by the participating parties
- Data can either be query by a connected client as well as sent to all connected clients by the server when a database update occurs
- Based on HTTP and REST, the following message structure shall be used:

**Requesting data from the server**:
```JSON
{
    "method": "get", // HTTP method
    "model": "league", // Django model to be queried
    "query": [ // Query parameter used for filtering data
        "id": 4, // Request league with id = 4
        "name__contains": "ThorsHero" // Request all leagues, which name contain the phrase "ThorsHero"
    ]
}
```

**Response data from the server**:
```JSON
{
    "status": "OK", // HTTP status
    "code": 200, // HTTP status code
    "model": "league", // Django model data in the response
    "partition": "single" / "partial" / "full", // Data Length: single model instance / partial list (based on query) / full list
    "data": [{...model}], / {...single_model} // Array of serialized models or a single serialized model
}
```
