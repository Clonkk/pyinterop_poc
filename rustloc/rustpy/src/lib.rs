use pyo3::prelude::*;
use numpy::{PyArrayLike2, TypeMustMatch, PyReadwriteArrayDyn};
use ndarray::ArrayViewMut;

// use rayon::iter::Zip;
// use numpy::ndarray::*;
// use num::{Float, NumCast};


#[allow(non_snake_case)]
fn doStuff(el: f64) -> f64{
  return (1.0 - el)/(1.0 + el)
}

// fn doStuff(el: &mut f64) -> f64{
//   return (1.0 - *el)/(1.0 + *el)
// }

#[allow(non_snake_case)]
#[pyfunction]
fn runCalc<'py>(_py: Python<'py>, array: PyArrayLike2<'py, f64, TypeMustMatch>) -> f64 {
    let s : f64 = array.as_array()
    .into_iter()
    .map(|value| {
        (1.0 - value)/(1.0 + value)
    })
    .sum();
    println!("{}", s);
    return s
}

#[allow(non_snake_case)]
#[pyfunction]
fn modArray<'py>(_py: Python<'py>, mut array:PyReadwriteArrayDyn<'py, f64>) {
    let mut ar = array.as_array_mut();
    ar[[0, 0]] = 123.0;
    ar[[0, 1]] = -5.0;
}

#[allow(non_snake_case)]
#[pyfunction]
fn normalForOp<'py>(_py: Python<'py>, mut array:PyReadwriteArrayDyn<'py, f64>) {
    let ar = array.as_array_mut();
    for el in ar.into_iter() {
        *el = doStuff(*el)
    }
}

#[allow(non_snake_case)]
#[pyfunction]
fn indexedOp<'py>(_py: Python<'py>, mut array:PyReadwriteArrayDyn<'py, f64>) {
    let mut ar = array.as_array_mut();
    for (_index, el) in ar.indexed_iter_mut() {
        *el = doStuff(*el)
        // ar[index] = doStuff(ar2[index])
    }
}

#[pyfunction]
#[allow(non_snake_case)]
fn parallelForOp<'py>(_py: Python<'py>, mut array:PyReadwriteArrayDyn<'py, f64>) {
    // Not in parallel yet
    // TODO run Rayon iterator on as_array_mut
    let mut ar = array.as_array_mut();
    ar.into_iter().for_each(|el| {
        *el = doStuff(*el)
    });
}

#[allow(non_snake_case)]
#[pyfunction]
fn parallelIndexedForOp<'py>(_py: Python<'py>, mut array:PyReadwriteArrayDyn<'py, f64>) {
    // Not in parallel yet
    // TODO run Rayon iterator on as_array_mut
    let mut ar = array.as_array_mut();
    ar.indexed_iter_mut().for_each(|(_index, el)| {
        *el = doStuff(*el)
    });
}

#[allow(non_snake_case)]
#[pymodule]
fn examply_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(runCalc, m)?)?;
    m.add_function(wrap_pyfunction!(modArray, m)?)?;
    m.add_function(wrap_pyfunction!(normalForOp, m)?)?;
    m.add_function(wrap_pyfunction!(indexedOp, m)?)?;
    m.add_function(wrap_pyfunction!(parallelForOp, m)?)?;
    m.add_function(wrap_pyfunction!(parallelIndexedForOp, m)?)?;
    Ok(())
}
