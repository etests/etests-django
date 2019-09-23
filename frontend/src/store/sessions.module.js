import { sessionService } from "@/api/session.service";

var session;

try {
  session = JSON.parse(localStorage.getItem("session")) || null;
} catch (err) {
  session = null;
  console.log(err);
}

if (session && session.completed) {
  JSON.parse(localStorage.removeItem("session"));
  session = null;
}
const initialState = session
  ? {
      status: { exists: true },
      session,
      all: { items: [] }
    }
  : {
      status: {},
      session: null,
      all: { items: [] }
    };

export const sessions = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }, id) {
      commit("getRequest", id);
      sessionService.get(id).then(
        session => {
          commit("getSuccess", session);
          setTimeout(() => {
            dispatch("alert/success", `Starting ${session.test.name}...`, {
              root: true
            });
          });
        },
        error => {
          commit("getFailure", error);
        }
      );
    },
    update({ dispatch, commit }, data) {
      commit("updateRequest", data);

      sessionService.update(data).then(
        data => {
          commit("updateSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Test submitted successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("updateFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    }
  },
  mutations: {
    getRequest(state) {
      state.status = { loading: true };
    },
    getSuccess(state, session) {
      state.status = { exists: true };
      state.session = session;
    },
    getFailure(state, error) {
      state.status = { error };
    },
    updateRequest(state, data) {
      state.status = { creating: true };
    },
    updateSuccess(state, data) {
      state.status = { created: true, session: data };
    },
    updateFailure(state, error) {
      state.status = { error: error };
    }
  }
};
