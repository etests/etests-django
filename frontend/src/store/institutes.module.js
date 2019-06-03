import { instituteService } from "@/api/institute.service";

export const institutes = {
  namespaced: true,
  state: {
    all: {}
  },
  actions: {
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
