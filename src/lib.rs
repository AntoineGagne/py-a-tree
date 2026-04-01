use pyo3::prelude::*;

#[pymodule]
mod py_a_tree {
    use std::sync::{Arc, Mutex};

    use a_tree::{ATree, AttributeDefinition, Event, EventError};
    use pyo3::exceptions::PyRuntimeError;
    use pyo3::prelude::*;

    #[pyclass(name = "AttributeDefinition")]
    #[derive(Clone)]
    pub struct PyAttributeDefinition(AttributeDefinition);

    #[pymethods]
    impl PyAttributeDefinition {
        #[staticmethod]
        pub fn boolean(name: &str) -> Self {
            Self(AttributeDefinition::boolean(name))
        }

        #[staticmethod]
        pub fn integer(name: &str) -> Self {
            Self(AttributeDefinition::integer(name))
        }

        #[staticmethod]
        pub fn float(name: &str) -> Self {
            Self(AttributeDefinition::float(name))
        }

        #[staticmethod]
        pub fn string(name: &str) -> Self {
            Self(AttributeDefinition::string(name))
        }

        #[staticmethod]
        pub fn integer_list(name: &str) -> Self {
            Self(AttributeDefinition::integer_list(name))
        }

        #[staticmethod]
        pub fn string_list(name: &str) -> Self {
            Self(AttributeDefinition::string_list(name))
        }

        fn __repr__(&self) -> String {
            format!("{:?}", self.0)
        }
    }

    #[derive(Clone, Debug)]
    enum Assignment {
        Boolean(String, bool),
        Integer(String, i64),
        Float(String, i64, u32), // mantissa, scale
        String(String, String),
        IntegerList(String, Vec<i64>),
        StringList(String, Vec<String>),
        Undefined(String),
    }

    #[pyclass(name = "EventBuilder")]
    pub struct PyEventBuilder {
        atree: Arc<Mutex<ATree<u64>>>,
        assignments: Vec<Assignment>,
    }

    #[pymethods]
    impl PyEventBuilder {
        pub fn with_boolean(&mut self, name: &str, value: bool) -> PyResult<()> {
            self.assignments
                .push(Assignment::Boolean(name.to_owned(), value));
            Ok(())
        }

        pub fn with_integer(&mut self, name: &str, value: i64) -> PyResult<()> {
            self.assignments
                .push(Assignment::Integer(name.to_owned(), value));
            Ok(())
        }

        pub fn with_float(&mut self, name: &str, mantissa: i64, scale: u32) -> PyResult<()> {
            self.assignments
                .push(Assignment::Float(name.to_owned(), mantissa, scale));
            Ok(())
        }

        pub fn with_string(&mut self, name: &str, value: &str) -> PyResult<()> {
            self.assignments
                .push(Assignment::String(name.to_owned(), value.to_owned()));
            Ok(())
        }

        pub fn with_integer_list(&mut self, name: &str, value: Vec<i64>) -> PyResult<()> {
            self.assignments
                .push(Assignment::IntegerList(name.to_owned(), value));
            Ok(())
        }

        pub fn with_string_list(&mut self, name: &str, values: Vec<String>) -> PyResult<()> {
            self.assignments
                .push(Assignment::StringList(name.to_owned(), values));
            Ok(())
        }

        pub fn with_undefined(&mut self, name: &str) -> PyResult<()> {
            self.assignments
                .push(Assignment::Undefined(name.to_owned()));
            Ok(())
        }

        pub fn build(&self) -> PyResult<PyEvent> {
            let guard = self.atree.lock().map_err(|e| atree_err(e.to_string()))?;
            let mut builder = guard.make_event();

            for assignment in &self.assignments {
                let result = match assignment {
                    Assignment::Boolean(name, value) => builder.with_boolean(name, *value),
                    Assignment::Integer(name, value) => builder.with_integer(name, *value),
                    Assignment::Float(name, number, scale) => {
                        builder.with_float(name, *number, *scale)
                    }
                    Assignment::String(name, value) => builder.with_string(name, value),
                    Assignment::IntegerList(name, values) => {
                        builder.with_integer_list(name, values)
                    }
                    Assignment::StringList(name, values) => {
                        let as_str: Vec<&str> = values.iter().map(String::as_str).collect();
                        builder.with_string_list(name, &as_str)
                    }
                    Assignment::Undefined(name) => builder.with_undefined(name),
                };
                result.map_err(event_err)?;
            }

            Ok(PyEvent(builder.build().map_err(event_err)?))
        }

        fn __repr__(&self) -> String {
            format!("EventBuilder(assignments={})", self.assignments.len())
        }
    }

    #[pyclass(name = "Event")]
    pub struct PyEvent(Event);

    #[pymethods]
    impl PyEvent {
        fn __repr__(&self) -> String {
            "Event(...)".to_owned()
        }
    }

    #[pyclass(name = "Report")]
    pub struct PyReport(Vec<u64>);

    #[pymethods]
    impl PyReport {
        pub fn matches(&self) -> Vec<u64> {
            self.0.clone()
        }

        fn __repr__(&self) -> String {
            format!("Report(matches={:?})", self.0)
        }
    }

    #[pyclass(name = "ATree")]
    pub struct PyATree(Arc<Mutex<ATree<u64>>>);

    #[pymethods]
    impl PyATree {
        #[new]
        pub fn new(definitions: Vec<PyRef<PyAttributeDefinition>>) -> PyResult<Self> {
            let definitions: Vec<AttributeDefinition> = definitions
                .iter()
                .map(|definition| definition.0.clone())
                .collect();
            let atree = ATree::new(&definitions).map_err(atree_err)?;
            Ok(Self(Arc::new(Mutex::new(atree))))
        }

        pub fn insert(&self, subscription_id: u64, expression: &str) -> PyResult<()> {
            let mut guard = self.0.lock().map_err(|e| atree_err(e.to_string()))?;
            guard
                .insert(&subscription_id, expression)
                .map_err(atree_err)
        }

        pub fn delete(&self, subscription_id: u64) -> PyResult<()> {
            let mut guard = self.0.lock().map_err(|e| atree_err(e.to_string()))?;
            guard.delete(&subscription_id);
            Ok(())
        }

        pub fn make_event(&self) -> PyResult<PyEventBuilder> {
            Ok(PyEventBuilder {
                atree: Arc::clone(&self.0),
                assignments: Vec::new(),
            })
        }

        pub fn search(&self, event: &PyEvent) -> PyResult<PyReport> {
            let guard = self.0.lock().map_err(|e| atree_err(e.to_string()))?;
            let report = guard.search(&event.0).map_err(atree_err)?;
            Ok(PyReport(
                report.matches().iter().copied().copied().collect(),
            ))
        }

        pub fn to_graphviz(&self) -> PyResult<String> {
            let guard = self.0.lock().map_err(|e| atree_err(e.to_string()))?;
            Ok(guard.to_graphviz())
        }

        fn __repr__(&self) -> String {
            "ATree(...)".to_owned()
        }
    }

    fn atree_err(e: impl std::fmt::Debug) -> PyErr {
        PyRuntimeError::new_err(format!("{e:?}"))
    }

    fn event_err(e: EventError) -> PyErr {
        PyRuntimeError::new_err(format!("{e:?}"))
    }
}
