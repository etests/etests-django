import { instituteService } from "@/api/institute.service";

export const institutes = {
  namespaced: true,
  state: {
    status: {},
    following: [],
    all: {}
  },
  actions: {
    getFollowing({ dispatch, commit }) {
      commit("followRequest");
      instituteService.getFollowing().then(
        institutes => {
          commit("getFollowingSuccess", institutes);
        },
        error => {
          commit("getFollowingFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    follow({ dispatch, commit }, id) {
      commit("followRequest", id);
      instituteService.follow(id).then(
        message => {
          commit("followSuccess", { id, message });
        },
        error => {
          commit("followFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    getAll({ commit }) {
      commit("getAllRequest");

      instituteService
        .getAll()
        .then(
          institutes => commit("getAllSuccess", institutes),
          error => commit("getAllFailure", error)
        );
    }
  },
  mutations: {
    followRequest(state, id) {
      state.status = { following: true, id: id };
    },
    followSuccess(state, data) {
      state.status = { followed: true, message: data.message, id: data.id };
      this.dispatch("users/followInstitute", data.id);
    },
    followFailure(state, error) {
      state.status = { error: error };
    },
    getAllRequest(state) {
      state.status = { loading: true };
    },
    getAllSuccess(state, institutes) {
      state.status = {};
      state.all = { items: institutes };
    },
    getAllFailure(state, error) {
      state.status = { error };
    },
    getFollowingRequest(state) {
      state.status = { loading: true };
    },
    getFollowingSuccess(state, institutes) {
      state.following = institutes;
    },
    getFollowingFailure(state, error) {
      state.status = { error };
    }
  }
};
