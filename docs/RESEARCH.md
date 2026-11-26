# Research and data sources

This register identifies candidate sources and tools. It is not an endorsement of every dataset or a statement that data has already been downloaded. Check current product documentation, licence, access conditions, resolution, and suitability before use.

## Geospatial and terrain

| Source | Potential use | Checks required |
|---|---|---|
| [IGN Spain](https://www.ign.es/) / [CNIG](https://centrodedescargas.cnig.es/) | Spanish mapping, elevation and geographic reference products | Product-specific licence, CRS, vertical datum, resolution, update date |
| [Copernicus Land Monitoring Service](https://land.copernicus.eu/) | Land cover and related environmental layers | Product terms, spatial/temporal resolution, attribution |
| [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) | Earth observation data discovery and access | Collection-specific terms, processing level, cloud/coverage constraints |

## Weather and environmental context

| Source | Potential use | Checks required |
|---|---|---|
| [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/) | ERA5 reanalysis and related climate datasets | Dataset-specific terms, grid spacing, temporal cadence, variable definitions |
| [AEMET OpenData](https://opendata.aemet.es/) | Spanish meteorological observations and products where available | API terms, station coverage, access limits, observation metadata |
| [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/) | Active-fire detections as contextual observations | Product confidence, overpass timing, resolution, latency, licence and interpretation |

ERA5 is a reanalysis product, not a local ground-truth weather station. AEMET station observations are spatially discrete and may not represent conditions at the simulated location. Satellite active-fire detections are observations with resolution, timing, and detection limitations; they are not a complete fire perimeter truth set.

## Simulation and robotics

| Project | Potential role | Official reference |
|---|---|---|
| NVIDIA Isaac Sim | Scene, sensors, simulation runtime | [Isaac Sim documentation](https://docs.isaacsim.omniverse.nvidia.com/) |
| ROS 2 | Robotics middleware and message integration | [ROS 2 documentation](https://docs.ros.org/) |
| PX4 | Autopilot software and SITL experiments | [PX4 documentation](https://docs.px4.io/) |
| OpenVINO | Inference runtime and device experimentation | [OpenVINO documentation](https://docs.openvino.ai/) |

Pin versions only after testing the exact combination. Confirm supported operating systems, GPU/driver requirements, simulator bridges, middleware distributions, and licence terms.

## Data and model selection checklist

For each external artefact, record:
- provider and canonical product/model name;
- version, release date, and retrieval date;
- URL or stable identifier;
- licence and attribution obligations;
- geographic and temporal coverage;
- spatial resolution and measurement units;
- known quality flags and limitations;
- checksum for downloaded immutable artefacts;
- any transformations applied locally.

## Scientific and operational boundary

A digital scene can provide geographic context and support software integration tests. It does not prove that the environmental model is physically valid. Any wildfire spread model should be selected and reviewed separately, with documented equations, input requirements, calibration data, validation studies, uncertainty, and domain limitations. Do not infer model validity from realistic-looking flames, smoke, or drone motion.
