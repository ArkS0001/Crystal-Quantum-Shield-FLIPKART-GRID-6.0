![Screenshot 2024-09-01 at 03-50-13 FinalSolution - Dashboards - Grafana](https://github.com/user-attachments/assets/585ac234-a2f9-4d70-a285-64fb5ec93755)


 Set Up Prometheus

Create Prometheus Configuration File (prometheus.yml):

yaml

global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'securityserver'
    static_configs:
      - targets: ['localhost:8002']  # The address where metrics are exposed

Run Prometheus:

Download and run Prometheus:

bash

./prometheus --config.file=prometheus.yml

4. Set Up Grafana

Install Grafana:

Download and install Grafana from the Grafana website.

Configure Grafana:

    Add Prometheus as a Data Source:
        Open Grafana in your browser (usually at http://localhost:3000).
        Go to Configuration > Data Sources.
        Click Add data source and select Prometheus.
        Set the URL to http://localhost:9090 (default Prometheus URL) and click Save & Test.

    Create Dashboards:
        Go to Create > Dashboard.
        Click Add new panel.
        Use Prometheus queries to visualize metrics. For example, to visualize the total number of requests:

        promql

        requests_total

        Configure the visualization options as needed and save the dashboard.

5. Verify and Monitor

    Check Metrics:
        Ensure that metrics are being collected by Prometheus. You can verify this by visiting http://localhost:9090/targets to see if the securityserver target is being scraped.

    View Dashboards:
        Open Grafana dashboards to visualize the metrics. You should see graphs and data based on the metrics exposed by securityserver.

Summary

    Expose metrics from your securityserver using prometheus_client.
    Configure Prometheus to scrape these metrics.
    Set up Grafana to visualize the metrics from Prometheus.
