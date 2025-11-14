from fastapi import APIRouter

from app.core.dependency import DependPermission

from .configs import configs_router
from .dashboard import dashboard_router
from .tenderReview import tenderReview_router
from .searchDocument import searchDocument_router
from .clauseRecommender import clauseRecommender_router
from .reviewCriteria import reviewCriteria_router
from .criteriaProfile import criteriaProfile_router
from .userManagement import userManagement_router
from .about import about_router
from .apis import apis_router
from .auditlog import auditlog_router
from .base import base_router
from .depts import depts_router
from .menus import menus_router
from .roles import roles_router
from .users import users_router

v1_router = APIRouter()

v1_router.include_router(base_router, prefix="/base")
v1_router.include_router(configs_router, prefix="/configs")
v1_router.include_router(dashboard_router, prefix="/dashboard")
v1_router.include_router(tenderReview_router, prefix="/tender-review", dependencies=[DependPermission])
v1_router.include_router(searchDocument_router, prefix="/search-document", dependencies=[DependPermission])
v1_router.include_router(clauseRecommender_router, prefix="/clause-recommender", dependencies=[DependPermission])
v1_router.include_router(reviewCriteria_router, prefix="/review-criteria", dependencies=[DependPermission])
v1_router.include_router(criteriaProfile_router, prefix="/criteria-profile", dependencies=[DependPermission])
v1_router.include_router(userManagement_router, prefix="/user-management", dependencies=[DependPermission])
v1_router.include_router(about_router, prefix="/about")
v1_router.include_router(users_router, prefix="/user", dependencies=[DependPermission])
v1_router.include_router(roles_router, prefix="/role", dependencies=[DependPermission])
v1_router.include_router(menus_router, prefix="/menu", dependencies=[DependPermission])
v1_router.include_router(apis_router, prefix="/api", dependencies=[DependPermission])
v1_router.include_router(depts_router, prefix="/dept", dependencies=[DependPermission])
v1_router.include_router(auditlog_router, prefix="/auditlog", dependencies=[DependPermission])
