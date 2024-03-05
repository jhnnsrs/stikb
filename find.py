import wandb

#find the runs for the project
runs = wandb.Api(api_key="436cc46ef229c64af33d290f0047a854a1e5f22e").runs("my-awesome-project")

# print the run names
print([run.name for run in runs])