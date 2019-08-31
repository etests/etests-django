import { instituteService } from "@/api/institute.service";

export const institutes = {
  namespaced: true,
  state: {
    status: {},
    all: {}
  },
  actions: {
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
    },
    followFailure(state, error) {
      state.status = { error: error };
    },
    getAllRequest(state) {
      state.all = { loading: true };
    },
    getAllSuccess(state, institutes) {
      state.all = { items: institutes };
    },
    getAllFailure(state, error) {
      state.all = { error };
    }
  }
};
