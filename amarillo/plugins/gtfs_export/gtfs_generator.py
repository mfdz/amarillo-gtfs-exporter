from fastapi import FastAPI
from amarillo.plugins.gtfs_export.router import router

def setup(app : FastAPI):
	app.include_router(router)