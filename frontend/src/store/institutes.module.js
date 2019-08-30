import { instituteService } from "@/api/institute.service";

export const institutes = {
  namespaced: true,
  state: {
    status: {},
    all: {}
  },
  actions: {
    join({ dispatch, commit }, id) {
      commit("joinRequest", id);
      instituteService.join(id).then(
        message => {
          commit("joinSuccess", { id, message });
        },
        error => {
          commit("joinFailure", error);
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
    joinRequest(state, id) {
      state.status = { joining: true, id: id };
    },
    joinSuccess(state, data) {
      state.status = { joined: true, message: data.message, id: data.id };
    },
    joinFailure(state, error) {
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
