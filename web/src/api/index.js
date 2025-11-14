import { request } from '@/utils'
import { get, set } from 'lodash-es'
import qs from 'qs'




export default {
  login: (data) => request.post('/base/access_token', data, { noNeedToken: true }),
  getUserInfo: () => request.get('/base/userinfo'),
  getUserMenu: () => request.get('/base/usermenu'),
  getUserApi: () => request.get('/base/userapi'),
  // config
  getPageConfig: (page) => request.get(`/configs/${page}`),
  // dashboard
  getDashboardData: (params = {}) => request.get('/dashboard/list', { params}),
  // tender-review
  uploadFiles: (formData) => request.post(
    '/tender-review/upload', 
    formData, 
    { headers: { 'Content-Type': 'multipart/form-data' } }
  ),

  deleteFile: (data) => {
    const fd = new FormData()
    fd.append('filename', data.filename)
    fd.append('folder', data.folder)
    return request.post('/tender-review/delete', fd)
  },
  getChecklist: (params = {}) =>
    request.get('/tender-review/analysis-checklist', {
      params,
      paramsSerializer: (p) => qs.stringify(p, { arrayFormat: 'repeat' })
  }),
  submitTenderReview: (data) => request.post('/tender-review/submit-review', data),


  // search-document
  searchDocument: (params = {}) => request.get(`/search-document`, { params }),

  // clause-recommender
  getRecommendations: (params = {}) => request.get(`/clause-recommender`, { params }),
  updateRecommendation: (data) => request.put(`/clause-recommender/update`, data),


  // review-criteria
  getReviewCriteria: (params = {}) => request.get(`/review-criteria`, { params }),
  deleteReviewItem: (id) => request.delete(`/review-criteria/${id}`),
  // criteria-profile
  getCriteriaProfile: (params = {}) => request.get('/criteria-profile', { params }),
  createCriteriaProfile: (data = {}) => request.post('/criteria-profile', data),
  updateCriteriaProfile: (data = {}) => request.post('/criteria-profile', data),

  // user-management
  getUserManagementData: (page) => request.get(`/user-management/${page}`),

  //about
  getAboutAnalysis: () => request.get('/about'),

  
  // profile
  updatePassword: (data = {}) => request.post('/base/update_password', data),
  // users
  getUserList: (params = {}) => request.get('/user/list', { params }),
  getUserById: (params = {}) => request.get('/user/get', { params }),
  createUser: (data = {}) => request.post('/user/create', data),
  updateUser: (data = {}) => request.post('/user/update', data),
  deleteUser: (params = {}) => request.delete(`/user/delete`, { params }),
  resetPassword: (data = {}) => request.post(`/user/reset_password`, data),
  // role
  getRoleList: (params = {}) => request.get('/role/list', { params }),
  createRole: (data = {}) => request.post('/role/create', data),
  updateRole: (data = {}) => request.post('/role/update', data),
  deleteRole: (params = {}) => request.delete('/role/delete', { params }),
  updateRoleAuthorized: (data = {}) => request.post('/role/authorized', data),
  getRoleAuthorized: (params = {}) => request.get('/role/authorized', { params }),
  // menus
  getMenus: (params = {}) => request.get('/menu/list', { params }),
  createMenu: (data = {}) => request.post('/menu/create', data),
  updateMenu: (data = {}) => request.post('/menu/update', data),
  deleteMenu: (params = {}) => request.delete('/menu/delete', { params }),
  // apis
  getApis: (params = {}) => request.get('/api/list', { params }),
  createApi: (data = {}) => request.post('/api/create', data),
  updateApi: (data = {}) => request.post('/api/update', data),
  deleteApi: (params = {}) => request.delete('/api/delete', { params }),
  refreshApi: (data = {}) => request.post('/api/refresh', data),
  // depts
  getDepts: (params = {}) => request.get('/dept/list', { params }),
  createDept: (data = {}) => request.post('/dept/create', data),
  updateDept: (data = {}) => request.post('/dept/update', data),
  deleteDept: (params = {}) => request.delete('/dept/delete', { params }),
  // auditlog
  getAuditLogList: (params = {}) => request.get('/auditlog/list', { params }),
}
