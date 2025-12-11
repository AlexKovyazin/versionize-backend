from polyfactory.factories.pydantic_factory import ModelFactory

from bff.src import domain


class CompanyFactory(ModelFactory[domain.company.Company]):
    __model__ = domain.company.Company


class DocumentFactory(ModelFactory[domain.document.DocumentOut]):
    __model__ = domain.document.DocumentOut


class NotificationFactory(ModelFactory[domain.notification.NotificationOut]):
    __model__ = domain.notification.NotificationOut


class ProjectFactory(ModelFactory[domain.project.ProjectOut]):
    __model__ = domain.project.ProjectOut


class RemarkFactory(ModelFactory[domain.remark.RemarkOut]):
    __model__ = domain.remark.RemarkOut


class RemarkDocFactory(ModelFactory[domain.remark_doc.RemarkDocOut]):
    __model__ = domain.remark_doc.RemarkDocOut


class SectionFactory(ModelFactory[domain.section.SectionOut]):
    __model__ = domain.section.SectionOut


class DefaultSectionFactory(ModelFactory[domain.section.DefaultSectionOut]):
    __model__ = domain.section.DefaultSectionOut


class UserFactory(ModelFactory[domain.user.User]):
    __model__ = domain.user.User


ENTITY_FACTORIES = {
    domain.company.Company: CompanyFactory,
    domain.document.DocumentOut: DocumentFactory,
    domain.notification.NotificationOut: NotificationFactory,
    domain.project.ProjectOut: ProjectFactory,
    domain.remark.RemarkOut: RemarkFactory,
    domain.remark_doc.RemarkDocOut: RemarkDocFactory,
    domain.section.SectionOut: SectionFactory,
    domain.section.DefaultSectionOut: DefaultSectionFactory,
    domain.user.User: UserFactory,
}
