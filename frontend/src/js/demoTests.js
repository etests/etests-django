export const demoTests = {
  tests: [
    {
      id: 0,
      name: "Demo Test 1",
      practice: true,
      time_alotted: "03:00:00",
      sections: [
        {
          end: 3,
          start: 0,
          subject: "Physics",
          subjectIndex: 0
        },
        {
          end: 6,
          start: 4,
          subject: "Mathematics",
          subjectIndex: 1
        },
        {
          end: 7,
          start: 7,
          subject: "Chemistry",
          subjectIndex: 2
        }
      ],
      questions: [
        {
          text: "Significant  figures  in  3400  are-",
          type: 0,
          image: null,
          topic: "Rotational Motion",
          status: 3,
          answers: ["Answer P", "Answer Q", "Answer R", "Answer S", "Answer T"],
          options: ["2", "5", "6", "7"],
          section: 0,
          topicIndex: 5,
          correctMarks: 4,
          partialMarks: 0,
          incorrectMarks: 1
        },
        {
          text:
            "A student performed the experiment of  determination  of  focal  length  of  a  concave  mirror  by  u-v  method  using\nan  optical  bench  of  length  1.5  meter.  The  focal length of the mirror used is 24  m.  The  maximum  error  in  the\nlocation of  the image  can  0.2  m.  The  5 sets  of  (u,  v)  values  recorded  by  the  student  (in  cm)  are  :  (42, 56),  (48,\n48),(60,  40),  (66,  33),  (78,  39).  The  data  set(s)  that  connot  come  from  experiment  and  is  (are)  incorrectly\nrecorded  is  (are  )",
          type: 1,
          image: null,
          topic: "Physics and Measurement",
          status: 3,
          answers: ["Vector", "Scalar", "m", "m/s", "Tensor"],
          options: ["2", "-2", "6", "9"],
          section: 0,
          topicIndex: 0,
          correctMarks: 4,
          partialMarks: 1,
          incorrectMarks: 1
        },
        {
          text: "Value of g is",
          type: 2,
          image: null,
          topic: "Kinematics",
          status: 3,
          answers: ["Vector", "Scalar", "m", "m/s", "Tensor"],
          options: ["2", "-2", "6", "9"],
          section: 0,
          topicIndex: 1,
          correctMarks: 4,
          partialMarks: 0,
          incorrectMarks: 1
        },
        {
          text: "Mark The Corrrect",
          type: 3,
          image: null,
          topic: "Kinematics",
          status: 3,
          answers: ["Vector", "Scalar", "m", "m/s", "Tensor"],
          options: ["2", "-2", "6", "9"],
          section: 0,
          topicIndex: 1,
          correctMarks: 4,
          partialMarks: 2,
          incorrectMarks: 1
        },
        {
          text: "Square Root of 4 is",
          type: 0,
          image: null,
          topic: "Sets, relations and functions",
          status: 3,
          answers: ["Vector", "Scalar", "m", "m/s", "Tensor"],
          options: ["2", "-2", "6", "9"],
          section: 1,
          topicIndex: 0,
          correctMarks: 4,
          partialMarks: 0,
          incorrectMarks: 1
        },
        {
          text: "4 times 2 is",
          type: 2,
          image: null,
          topic: "Matrices and determinants",
          status: 3,
          answers: ["Vector", "Scalar", "m", "m/s", "Tensor"],
          options: ["2", "-2", "6", "9"],
          section: 1,
          topicIndex: 2,
          correctMarks: 4,
          partialMarks: 0,
          incorrectMarks: 1
        },
        {
          text:
            "A bag contains 4 red and 6 black balls. A ball is drawn at random from the bag, its colour is observed and this ball along with two additional balls of the same colour are returned to the bag. If now a ball is drawn at random from the bag, then the probability that this drawn ball is red. Which is Incorrect?",
          type: 1,
          image: null,
          topic: "Permutations and combinations",
          status: 3,
          answers: ["Vector", "Scalar", "m", "m/s", "Tensor"],
          options: ["2", "-2", "6", "9"],
          section: 1,
          topicIndex: 3,
          correctMarks: 4,
          partialMarks: 0,
          incorrectMarks: 1
        },
        {
          text:
            "A  student  performed  the  experiment  to  measure  the  speed  of  sound  in  air  using  resonance  air-column  method.\nTwo  resonances  in  the air-column  were obtained  by  resonance  and that  with  the  longer  air-column  is the  second\nresonance.  Then,",
          type: 0,
          image: null,
          topic: "Atomic Structure",
          status: 3,
          answers: ["Vector", "Scalar", "m", "m/s", "Tensor"],
          options: ["2", "-2", "6", "9"],
          section: 2,
          topicIndex: 2,
          correctMarks: 4,
          partialMarks: 0,
          incorrectMarks: 1
        }
      ],
      answers: [
        {
          answer: 0
        },
        {
          answer: [1, 2]
        },
        {
          answer: "9.8"
        },
        {
          answer: [[0, 2], [1, 2], [0, 3], [1, 3]]
        },
        {
          answer: 0
        },
        {
          answer: "8"
        },
        {
          answer: [1, 2, 3]
        },
        {
          answer: 0
        }
      ],
      institute: 1,
      registered_student: [1, 4],
      tags: []
    }
  ],
  getResult(session) {
    var responses = JSON.parse(JSON.stringify(session.response));
    var answers = session.test.answers;
    var noOfSections = session.test.sections.length;
    var maxMarks = [];
    var sectionWise = [];
    var currentQuestion = {};
    var questionWiseMarks = [];
    var topicWiseMarks = [];
    var i = 0;
    for (i = 0; i < noOfSections; i++) {
      maxMarks.push(0);
      sectionWise.push(0);
    }
    maxMarks.push(0);
    var marks = { total: 0, maxMarks, sectionWise };
    for (i = 0; i < session.test.questions.length; i++) {
      questionWiseMarks.push({ marks: 0, status: 0 });
    }
    for (i = 0; i < session.test.sections.length; i++) {
      topicWiseMarks.push({});
    }
    var report = {
      test: session.test,
      response: session.response,
      result: {},
      marks
    };
    report.test = session.test;
    for (i = 0; i < session.test.questions.length; i++) {
      currentQuestion = session.test.questions[i];
      marks.maxMarks[noOfSections] += currentQuestion.correctMarks;
      marks.maxMarks[currentQuestion.section] += currentQuestion.correctMarks;
      if (
        session.test.questions[i].type === 0 &&
        responses[i].answer.length !== 0
      ) {
        if (responses[i].answer === answers[i].answer) {
          questionWiseMarks[i].marks = currentQuestion.correctMarks;
          questionWiseMarks[i].status = 2;
          report.marks.total += currentQuestion.correctMarks;
          report.marks.sectionWise[currentQuestion.section] +=
            currentQuestion.correctMarks;
        } else if (responses[i].answer !== answers[i].answer) {
          questionWiseMarks[i].marks = -currentQuestion.incorrectMarks;
          questionWiseMarks[i].status = 1;
          report.marks.total -= currentQuestion.incorrectMarks;
          report.marks.sectionWise[currentQuestion.section] -=
            currentQuestion.incorrectMarks;
        }
      } else if (
        session.test.questions[i].type === 1 &&
        responses[i].answer.length !== 0
      ) {
        var arrayOfChildrenNames = responses[i].answer;
        var arrayOfFamilyMemberNames = answers[i].answer;
        var isarrayOfNamesSubsetOfFamily = arrayOfChildrenNames.every(function(
          val
        ) {
          return arrayOfFamilyMemberNames.indexOf(val) >= 0;
        });
        if (
          isarrayOfNamesSubsetOfFamily &&
          arrayOfChildrenNames.length < arrayOfFamilyMemberNames.length &&
          currentQuestion.partialMarks !== 0
        ) {
          report.marks.total +=
            arrayOfChildrenNames.length * currentQuestion.partialMarks;
          questionWiseMarks[i].marks =
            currentQuestion.partialMarks * arrayOfChildrenNames.length;
          questionWiseMarks[i].status = 3;
          report.marks.sectionWise[currentQuestion.section] +=
            currentQuestion.partialMarks * arrayOfChildrenNames.length;
        } else if (isarrayOfNamesSubsetOfFamily) {
          questionWiseMarks[i].marks = currentQuestion.correctMarks;
          questionWiseMarks[i].status = 2;
          report.marks.total += currentQuestion.correctMarks;
          report.marks.sectionWise[currentQuestion.section] +=
            currentQuestion.correctMarks;
        } else {
          questionWiseMarks[i].marks = -currentQuestion.incorrectMarks;
          questionWiseMarks[i].status = 1;
          report.marks.total -= currentQuestion.incorrectMarks;
          report.marks.sectionWise[currentQuestion.section] -=
            currentQuestion.incorrectMarks;
        }
      } else if (
        session.test.questions[i].type === 2 &&
        responses[i].answer.length !== 0
      ) {
        if (
          parseFloat(responses[i].answer) <=
            1.01 * parseFloat(answers[i].answer) &&
          parseFloat(responses[i].answer) >=
            0.99 * parseFloat(answers[i].answer)
        ) {
          questionWiseMarks[i].marks = currentQuestion.correctMarks;
          questionWiseMarks[i].status = 2;
          report.marks.total += currentQuestion.correctMarks;
          report.marks.sectionWise[currentQuestion.section] +=
            currentQuestion.correctMarks;
        } else {
          questionWiseMarks[i].marks = -currentQuestion.incorrectMarks;
          questionWiseMarks[i].status = 1;
          report.marks.total -= currentQuestion.incorrectMarks;
          report.marks.sectionWise[currentQuestion.section] -=
            currentQuestion.incorrectMarks;
        }
      } else if (
        session.test.questions[i].type === 3 &&
        responses[i].answer.length !== 0
      ) {
        // For Matrix match for each part status 0 means unanswered 1 means incorrect 2 means correct
        var responsesMatrix = responses[i].answer;
        var answersMatrix = answers[i].answer;
        var curMarks = [];
        for (var j = 0; j < responsesMatrix.length; j++) {
          curMarks.push({ marks: 0, status: 0 });
        }
        for (j = 0; j < responsesMatrix.length; j++) {
          if (responsesMatrix[j].length !== 0) {
            responsesMatrix[j].sort();
            answersMatrix[j].sort();
            console.log(responsesMatrix[j], answersMatrix[j]);
            console.log(responsesMatrix[j] === answersMatrix[j]);

            if (
              JSON.stringify(responsesMatrix[j]) ===
              JSON.stringify(answersMatrix[j])
            ) {
              curMarks[j]["marks"] = currentQuestion.partialMarks;
              curMarks[j]["status"] = 2;
            } else {
              curMarks[j]["marks"] = currentQuestion.incorrectMarks * -1;
              console.log("Matrix incorrect");
              curMarks[j]["status"] = 1;
            }
          }
        }
        var totalMatrixMarks = 0;
        var matrixMarks = [];
        var matrixStatus = [];
        for (j = 0; j < curMarks.length; j++) {
          totalMatrixMarks += curMarks[j]["marks"];
          matrixMarks.push(curMarks[j]["marks"]);
          matrixStatus.push(curMarks[j]["status"]);
        }
        questionWiseMarks[i].marks = matrixMarks;
        questionWiseMarks[i].status = matrixStatus;
        report.marks.total += totalMatrixMarks;
        report.marks.sectionWise[currentQuestion.section] += totalMatrixMarks;
      }
      var currentTopic = topicWiseMarks[session.test.questions[i].section];
      var curTopicMarks = 0;
      if (Array.isArray(questionWiseMarks[i].marks))
        curTopicMarks = questionWiseMarks[i].marks.reduce((a, b) => a + b, 0);
      else curTopicMarks = questionWiseMarks[i].marks;
      if (
        Object.prototype.hasOwnProperty.call(
          currentTopic,
          session.test.questions[i].topicIndex
        )
      )
        currentTopic[session.test.questions[i].topicIndex] += curTopicMarks;
      else currentTopic[session.test.questions[i].topicIndex] = curTopicMarks;
    }
    report.result.questionWiseMarks = questionWiseMarks;
    report.result.topicWiseMarks = topicWiseMarks;
    return report;
  },
  newSession(test) {
    var session = {
      response: [],
      test,
      isDemo: true,
      duration: test.time_alotted,
      checkin_time: new Date().toISOString(),
      current: { questionIndex: 0, sectionIndex: 0 },
      completed: false
    };
    for (var i = 0; i < test.questions.length; i++) {
      session.response.push({
        answer: [],
        status: i == 0 ? 1 : 0,
        timeElapsed: 0
      });
    }
    return session;
  }
};
