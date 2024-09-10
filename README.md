# Toxiproxy and Python HTTP Service

This project contains a simple Python HTTP service and a Toxiproxy instance to simulate network conditions. The Python service accepts any HTTP call with any payload and always responds with `200 OK`. Toxiproxy allows you to simulate network failures, latency, and other network conditions for testing.

## Project Structure

- **app.py**: Python HTTP service built with Flask.
- **Dockerfile**: Container configuration for the Python HTTP service.
- **docker-compose.yml**: Configuration for Docker Compose to run the Python service and Toxiproxy.
- **LICENSE.md**: MIT License file for the project.
- **toxiproxy**: A proxy service to simulate network conditions.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/trustlreis/chaos-http-endpoint.git
   cd chaos-http-endpoint
   ```

2. Build and start the services using Docker Compose:

   ```bash
   docker-compose up --build
   ```

   This will start two services:
   - **Toxiproxy** on port `8474` (for the API) and `8081` (for proxying traffic)
   - **HTTP Service** on port `8080`

### Usage

#### Sending Requests without Toxiproxy

You can send HTTP requests directly to the Python service, bypassing Toxiproxy.

1. **Directly to the HTTP Service:**

   ```bash
   curl -X GET http://localhost:8080/some-endpoint
   ```

   This will return `200 OK` for any HTTP method or payload.

   Example for a POST request with payload:

   ```bash
   curl -X POST http://localhost:8080/api/test -d '{"key": "value"}' -H "Content-Type: application/json"
   ```

   You will get a `200 OK` response along with the payload and headers printed in the logs.

#### Sending Requests through Toxiproxy

You can send requests to the Python service through Toxiproxy to simulate network conditions.

1. **Create a Proxy for the HTTP Service:**

   Use the following command to create a proxy that forwards traffic from `localhost:8081` to the Python service on `localhost:8080`:

   ```bash
   curl -X POST \
     --data '{"name": "http_service", "listen": "0.0.0.0:8081", "upstream": "http_service:8080"}' \
     http://localhost:8474/proxies
   ```

2. **Send Requests through Toxiproxy:**

   Once the proxy is set up, you can send requests through Toxiproxy:

   ```bash
   curl -X GET http://localhost:8081/some-endpoint
   ```

   This will forward the request through Toxiproxy to the Python service and return `200 OK`.

#### Adding Toxics to Test with Toxiproxy

Toxiproxy allows you to add "toxics" to simulate network failures, latency, and other issues. Here are some examples of how to add toxics.

1. **Add Latency to Requests:**

   To simulate a 100ms delay for all requests to the Python service, use the following command:

   ```bash
   curl -X POST \
     --data '{"type": "latency", "toxicity": 1.0, "attributes": {"latency": 100}}' \
     http://localhost:8474/proxies/http_service/toxics
   ```

   Now, any request sent through Toxiproxy will be delayed by 100ms.

   Example:

   ```bash
   curl -X GET http://localhost:8081/some-endpoint
   ```

2. **Simulate Bandwidth Limit:**

   To limit the bandwidth to 50KB/s, use the following command:

   ```bash
   curl -X POST \
     --data '{"type": "bandwidth", "toxicity": 1.0, "attributes": {"rate": 50000}}' \
     http://localhost:8474/proxies/http_service/toxics
   ```

   This will throttle the response from the Python service to 50KB/s.

3. **Simulate Connection Cutoff:**

   To simulate a connection cutoff where no data is sent:

   ```bash
   curl -X POST \
     --data '{"type": "limit_data", "toxicity": 1.0, "attributes": {"bytes": 0}}' \
     http://localhost:8474/proxies/http_service/toxics
   ```

   This will make the proxy stop forwarding any data to the Python service, effectively simulating a network failure.

4. **Remove a Toxic:**

   To remove a toxic from the proxy, use the following command:

   ```bash
   curl -X DELETE http://localhost:8474/proxies/http_service/toxics/{toxic_name}
   ```

   Replace `{toxic_name}` with the name of the toxic you want to remove (e.g., `latency`, `bandwidth`).

### Example: Simulating Network Failure and Latency

1. **Step 1: Create a Proxy:**

   ```bash
   curl -X POST \
     --data '{"name": "http_service", "listen": "0.0.0.0:8081", "upstream": "http_service:8080"}' \
     http://localhost:8474/proxies
   ```

2. **Step 2: Add a Toxic to Simulate a 500ms Latency:**

   ```bash
   curl -X POST \
     --data '{"type": "latency", "toxicity": 1.0, "attributes": {"latency": 500}}' \
     http://localhost:8474/proxies/http_service/toxics
   ```

3. **Step 3: Test with a Request:**

   Send a request through Toxiproxy:

   ```bash
   curl -X GET http://localhost:8081/some-endpoint
   ```

   This request will be delayed by 500ms before reaching the Python service.

4. **Step 4: Remove the Latency Toxic:**

   ```bash
   curl -X DELETE http://localhost:8474/proxies/http_service/toxics/latency
   ```

### Environment Variables

- `FLASK_ENV`: Set to `development` to enable debug mode in Flask.

### Ports

- `8080`: Python HTTP service.
- `8081`: Toxiproxy proxy for the HTTP service.
- `8474`: Toxiproxy API.

### Stopping the Services

To stop the services, use:

```bash
docker-compose down
```

## Additional Information

- [Toxiproxy Documentation](https://github.com/Shopify/toxiproxy#readme)
- [Flask Documentation](https://flask.palletsprojects.com/en/latest/)

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
