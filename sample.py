import dci_orm.model

dci = dci_orm.model.ORM()
Jobs = dci.base.classes.jobs
session = dci.session

for job in session.query(Jobs).all():
    print(job.team.name)
