import { unitTestService } from "@/api/unitTest.service";

const initialState = {
  status: {},
  test: {},
  all: { items: [] }
};

export const unitTests = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }, id) {
      commit("getRequest", id);

      unitTestService.get(id).then(
        test => {
          commit("getSuccess", test);
          setTimeout(() => {
            dispatch("alert/success", "Unit test fetched successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("getFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    create({ dispatch, commit }, data) {
      commit("createRequest", data);

      unitTestService.create(data).then(
        data => {
          commit("createSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Unit Test created successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("createFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    remove({ dispatch, commit }, id) {
      commit("removeRequest", id);

      unitTestService.remove(id).then(
        _ => {
          commit("removeSuccess", id);
          setTimeout(() => {
            dispatch("alert/success", "Unit Test removed successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("removeFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
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
    getRequest(state) {
      state.status = { loading: true };
    },
    getSuccess(state, test) {
      state.status = {};
      state.test = test;
    },
    getFailure(state, error) {
      state.status = { error };
    },
    getAllRequest(state) {
      state.all = { loading: true };
    },
    getAllSuccess(state, unitTests) {
      state.all = { items: unitTests };
    },
    getAllFailure(state, error) {
      state.all = { error };
    },
    createRequest(state, data) {
      state.status = { creating: true };
    },
    createSuccess(state, data) {
      state.all.items.push(data);
      state.status = { created: true, test: data };
    },
    createFailure(state, error) {
      state.status = { error: error };
    },
    removeRequest(state, id) {
      state.status = { removing: true, id: id };
    },
    removeSuccess(state, id) {
      state.status = { removed: true, id: id };
    },
    removeFailure(state, error) {
      state.status = { error: error };
    }
  }
};
