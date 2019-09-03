import { userService } from "@/api/user.service";

const user = JSON.parse(localStorage.getItem("user"));
const initialState = user
  ? { status: {}, user, all: {} }
  : { status: {}, user: null, all: {} };

export const users = {
  namespaced: true,
  state: initialState,
  actions: {
    updateProfile({ dispatch, commit }, data) {
      commit("updateProfileRequest");
      userService.updateProfile(data).then(data => {
        commit("updateProfileSuccess", data);
        setTimeout(() => {
          dispatch("alert/success", "Profile updated successfully!", {
            root: true
          });
        });
      });
    },
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
    updateProfileRequest(state, data) {
      state.status = { updating: true };
    },
    updateProfileSuccess(state, data) {
      state.status = { updated: true };
      state.user.profile = data;
      localStorage.user = JSON.stringify(state.user);
    },
    updateProfileFailure(state, error) {
      state.status = { error: error };
    },
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
      if (state.user.details && !state.user.details.following.includes(id)) {
        state.user.details.following.push(id);
        localStorage.user = JSON.stringify(state.user);
      }
    }
  }
};
