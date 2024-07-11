# amarillo-gtfs-exporter

This plugin for Amarillo adds endpoints `/region/{region_id}/gtfs` and `/region/{region_id}/gtfs-rt` for serving the GTFS data on your Amarillo instance. Serves the gtfs zip files from the `data/gtfs` folder. If the files don't exist or are out of date (from yesterday in the case of GTFS and older than a minute for GTFS-RT) the plugin will retrieve them from the configured `generator_url`. 

# Installation

```
pip install amarillo-gtfs-exporter
```

This package will install inside the amarillo/plugins folder in your python environment. Next time you launch Amarillo, it should be discovered automatically and you should see messages like this:

```
INFO - Discovered plugins: ['amarillo.plugins.gtfs_export', ...]
...
INFO - Running setup function for amarillo.plugins.gtfs_export
```

The `setup()` function will be called automatically and it will add the necessary endpoints to your Amarillo FastAPI application.

# Configuration

You can configure the `generator_url` through an environment variable, or by adding it to the `config` file in the amarillo root folder:

```
generator_url = 'http://localhost:8002'
```

The default value is `http://localhost:8002`.

The generator_url should point to a running instance of [amarillo-gtfs-generator](https://github.com/mfdz/amarillo-gtfs-generator/).


# Usage

Make GET requests to the `/region/{region_id}/gtfs` and `/region/{region_id}/gtfs-rt`. The GTFS data will be returned as a zip file, while realtime data can be requested in .pbf or .json using the format query parameter.

<!-- TODO: remove code that is unused because it has been moved to generator -->