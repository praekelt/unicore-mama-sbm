from cornice import Service

profiles = Service(
    name='profiles',
    path='/web/api/profiles.json',
    description="Manages stage based messaging profiles"
)


@profiles.get()
def get_profiles(request):
    return {'profiles': ['profile1', 'profile2']}
