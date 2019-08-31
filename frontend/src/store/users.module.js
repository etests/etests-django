import { userService } from "@/api/user.service";

const user = JSON.parse(localStorage.getItem("user"));
const initialState = user
  ? { status: {}, user, all: {} }
  : { status: {}, user: null, all: {} };
export const users = {
  namespaced: true,
  state: initialState,
  actions: {
    getAll({ commit }) {
      commit("getAllRequest");

      userService
        .getAll()
        .then(
          users => commit("getAllSuccess", users),
          error => commit("getAllFailure", error)
        );
    },
    followInstitute({ commit }, id) {
      commit("followInstituteSuccess", id);
    }
  },
  mutations: {
    getAllRequest(state) {
      state.all = { loading: true };
    },
    getAllSuccess(state, users) {
      state.all = { items: users };
    },
    getAllFailure(state, error) {
      state.all = { error };
    },
    followInstituteSuccess(state, id) {
      if (state.user.profile && !state.user.profile.following.includes(id)) {
        state.user.profile.following.push(id);
        localStorage.user = JSON.stringify(state.user);
      }
    }
  }
};
