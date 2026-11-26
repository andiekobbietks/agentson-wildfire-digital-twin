# Roadmap

This roadmap is a sequence of evidence gates, not a promise of delivery dates.

## Phase 0: Scope and evidence register
- [ ] Select one documented incident or label the scenario fully synthetic.
- [ ] Define geographic extent and timeline.
- [ ] Create dataset, model, and asset licence register.
- [ ] Record intended use and prohibited operational claims.
- [ ] Choose a version-control strategy for large assets (do not commit large raw datasets by default).

**Exit gate:** scenario brief and source register reviewed.

## Phase 1: Geospatial baseline
- [ ] Select terrain source and verify permitted use.
- [ ] Import a small terrain tile.
- [ ] Validate CRS, vertical datum, units, and alignment.
- [ ] Export a scene-ready representation with provenance metadata.

**Exit gate:** documented import report and known-point checks.

## Phase 2: Weather replay
- [ ] Select one historical weather source and time window.
- [ ] Build a normalisation adapter.
- [ ] Preserve missing values and source status.
- [ ] Align weather timestamps to simulation time.
- [ ] Test wind vector and unit conventions.

**Exit gate:** replay fixture and automated validation tests.

## Phase 3: Simulation and robotics smoke test
- [ ] Install and pin a compatible Isaac Sim environment.
- [ ] Create a minimal scene.
- [ ] Add one simulated aerial vehicle and one sensor.
- [ ] Connect ROS 2.
- [ ] Evaluate PX4 SITL only if the supported integration path is confirmed.

**Exit gate:** reproducible startup, sensor stream, and vehicle state capture.

## Phase 4: Perception
- [ ] Select a model with suitable licence and documented provenance.
- [ ] Build a replaceable inference adapter.
- [ ] Record model hash, version, device, and latency.
- [ ] Evaluate with labelled data and document domain limitations.

**Exit gate:** baseline metrics and failure-case review.

## Phase 5: AgentSON trace
- [ ] Map lifecycle and component events to a pinned AgentSON schema.
- [ ] Record provenance and configuration hashes.
- [ ] Validate event sequence and schema.
- [ ] Test local buffering and interrupted connectivity.
- [ ] Export an independently inspectable run bundle.

**Exit gate:** complete trace for one repeatable run.

## Phase 6: Evaluation and publication
- [ ] Repeat the scenario with controlled seeds/configuration.
- [ ] Run fault injection for missing weather, dropped messages, and reconnect.
- [ ] Publish metrics, limitations, and reproducibility instructions.
- [ ] Obtain domain-expert review before making claims beyond software integration.

**Exit gate:** public evaluation report with explicit validation boundary.

## Later research, not MVP
- Multi-vehicle coordination.
- More complex terrain and weather conditions.
- Coupled fire behaviour models selected through a separate scientific review.
- Live data adapters, only with a documented legal and safety basis.
- Field trials, only under separate regulatory, organisational, and safety approvals.
