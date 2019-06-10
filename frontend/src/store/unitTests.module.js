import { unitTestService } from "@/api/unitTest.service";

export const unitTests = {
  namespaced: true,
  state: {
    all: {}
  },
  actions: {
    getAll({ commit }) {
      commit("getAllRequest");

      unitTestService
        .getAll()
        .then(
          unitTests => commit("getAllSuccess", unitTests),
          error => commit("getAllFailure", error)
        );
    }
  },
  mutations: {
    getAllRequest(state) {
      state.all = { loading: true };
    },
    getAllSuccess(state, unitTests) {
      state.all = { items: unitTests };
    },
    getAllFailure(state, error) {
      state.all = { error };
    }
  }
};
