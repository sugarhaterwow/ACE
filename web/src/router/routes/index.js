import i18n from '~/i18n'
const { t } = i18n.global

const Layout = () => import('@/layout/index.vue')

export const basicRoutes = [
  {
    path: '/',
    redirect: '/workbench/overview', // 默认跳转到首页
    meta: { order: 0 },
  },
  {
    name: t('views.workbench.label_application'),
    path: '/workbench',
    component: Layout,
    children: [
      // {
      //   path: '',
      //   component: () => import('@/views/workbench/index.vue'),
      //   name: `${t('views.workbench.label_workbench')}Default`,
      //   meta: {
      //     title: t('views.workbench.label_workbench'),
      //     icon: 'icon-park-outline:workbench',
      //     affix: true,
      //   },
      // },
  
      {
        path: 'overview',
        name: 'WorkbenchOverview',
        component: () => import('@/views/workbench/dashboard/index.vue'),
        meta: {
          title: t('views.workbench.label_dashboard'),
          icon: 'mdi:view-dashboard-outline',
        },
      },
      {
        path: 'tender-review',
        name: 'WorkbenchTenderReview',
        component: () => import('@/views/workbench/tender-review/index.vue'),
        meta: {
          title: t('views.workbench.label_tender_review'),
          icon: 'mdi:clipboard-check-outline',
        },
      },
      {
        path: 'contract-review',
        name: 'WorkbenchContractReview',
        component: () => import('@/views/workbench/contract-review/index.vue'),
        meta: {
          title: t('views.workbench.label_contract_review'),
          icon: 'mdi:clipboard-check-outline',
        },
      },
      {
        path: 'search-document',
        name: 'WorkbenchSearchDocument',
        component: () => import('@/views/workbench/search-document/index.vue'),
        meta: {
          title: t('views.workbench.label_search_document'),
          icon: 'mdi:file-search-outline',
        },
      },
      {
        path: 'clause-recommender',
        name: 'WorkbenchClauseRecommender',
        component: () => import('@/views/workbench/clause-recommender/index.vue'),
        meta: {
          title: t('views.workbench.label_clause_recommender'),
          icon: 'mdi:lightbulb-outline',
        },
      },
      {
        path: 'default-review-criteria',
        name: 'WorkbenchDefaultReviewCriteria',
        component: () => import('@/views/workbench/review-criteria/index.vue'),
        meta: {
          title: t('views.workbench.label_default_review_criteria'),
          icon: 'mdi:check-decagram-outline',
        },
      },
      {
        path: 'review-profile',
        name: 'WorkbenchReviewProfile',
        meta: {
          title: t('views.workbench.label_review_profile'),
          icon: 'mdi:clipboard-text-outline',
        },
        children: [
          {
            path: 'tender', // 子路由
            name: 'WorkbenchReviewProfileTender',
            component: () => import('@/views/workbench/review-profile/tender.vue'),
            meta: {
              title: 'Tender',
              icon: 'mdi:file-document-edit-outline'
            },
          },
          {
            path: 'contract', // 子路由
            name: 'WorkbenchReviewProfileContract',
            component: () => import('@/views/workbench/review-profile/contract.vue'),
            meta: {
              title: 'Contract',
              icon: 'mdi:file-sign'
            },
          },
        ],
      },
      {
        path: 'user-management',
        name: 'WorkbenchUserManagement',
        component: () => import('@/views/workbench/user-management/index.vue'),
        meta: {
          title: t('views.workbench.label_user_management'),
          icon: 'mdi:account-group-outline',
        },
      }
    ],
    meta: { order: 1 },
  },
  {
    name: t('views.profile.label_profile'),
    path: '/profile',
    component: Layout,
    isHidden: true,
    children: [
      {
        path: '',
        component: () => import('@/views/profile/index.vue'),
        name: `${t('views.profile.label_profile')}Default`,
        meta: {
          title: t('views.profile.label_profile'),
          icon: 'user',
          affix: true,
        },
      },
    ],
    meta: { order: 99 },
  },
  {
    name: 'ErrorPage',
    path: '/error-page',
    component: Layout,
    redirect: '/error-page/404',
    isHidden: true,
    meta: {
      title: t('views.errors.label_error'),
      icon: 'mdi:alert-circle-outline',
      order: 99,
    },
    children: [
      {
        name: 'ERROR-401',
        path: '401',
        component: () => import('@/views/error-page/401.vue'),
        meta: {
          title: '401',
          icon: 'material-symbols:authenticator',
        },
      },
      {
        name: 'ERROR-403',
        path: '403',
        component: () => import('@/views/error-page/403.vue'),
        meta: {
          title: '403',
          icon: 'solar:forbidden-circle-line-duotone',
        },
      },
      {
        name: 'ERROR-404',
        path: '404',
        component: () => import('@/views/error-page/404.vue'),
        meta: {
          title: '404',
          icon: 'tabler:error-404',
        },
      },
      {
        name: 'ERROR-500',
        path: '500',
        component: () => import('@/views/error-page/500.vue'),
        meta: {
          title: '500',
          icon: 'clarity:rack-server-outline-alerted',
        },
      },
    ],
  },
  {
    name: '403',
    path: '/403',
    component: () => import('@/views/error-page/403.vue'),
    isHidden: true,
  },
  {
    name: '404',
    path: '/404',
    component: () => import('@/views/error-page/404.vue'),
    isHidden: true,
  },
  {
    name: 'Login',
    path: '/login',
    component: () => import('@/views/login/index.vue'),
    isHidden: true,
    meta: {
      title: '登录页',
    },
  },
]

export const NOT_FOUND_ROUTE = {
  name: 'NotFound',
  path: '/:pathMatch(.*)*',
  redirect: '/404',
  isHidden: true,
}

export const EMPTY_ROUTE = {
  name: 'Empty',
  path: '/:pathMatch(.*)*',
  component: null,
}
  

const modules = import.meta.glob('@/views/**/route.js', { eager: true })
const asyncRoutes = []
Object.keys(modules).forEach((key) => {
  asyncRoutes.push(modules[key].default)
})

// 加载 views 下每个模块的 index.vue 文件
const vueModules = import.meta.glob('@/views/**/index.vue')

export { asyncRoutes, vueModules }
