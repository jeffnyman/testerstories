require "sinatra"

get '/' do
  erb :index
end

__END__
@@index
<!DOCTYPE html>
<html dir="ltr" lang="en">
<head>
  <meta charset="utf-8">
  <title>Triangle Tester</title>
</head>
<body>

<script>
  
  var side1;
  var side2;
  var side3;
  
  var side1Val;
  var side2Val;
  var side3Val;
  
  var checkNoInput = 0;
  var checkEmpty = 0;
  var checkNonNumeric = 0;
  var negativeSide = 0;
  var zeroSide = 0;
  var invalidSides = 0;
  var largeSides = 0;
  var checkScalene = 0;
  var checkEquilateral = 0;
  var checkIsosceles = 0;
  
  function evalData()
  {
    var value = 0;
    
    document.getElementById('response').innerHTML = "<strong>Response</strong>"
    side1 = document.getElementById('side1').value
    side2 = document.getElementById('side2').value
    side3 = document.getElementById('side3').value
    
    value = checkNoInputCases();
    
    if (value == 0) {
      return;
    } else {
      value = checkWhitespaceCases();
      if (value == 0) {
        return
      } else {
        value = checkNonNumericCases();
        if (value == 0) {
          return;
        }
      }
    }
    
    side1Val = side1 * 1;
    side2Val = side2 * 1;
    side3Val = side3 * 1;
    
    value = checkNegativeCases();
    if (value == 0) {
      return;
    } else {
      value = checkZeroLengthCases();
      if (value == 0) {
        return;
      } else {
        value = checkInvalidTriangleCases();
        if (value == 0) {
          return;
        } else {
          value = checkLargeSideCases();
          if (value == 0) {
            return;
          } else {
            value = checkScaleneCases();
            if (value == 0) {
              return;
            } else {
              value = checkEquilateralCases();
              if (value == 0) {
                return;
              } else {
                value = checkIsoscelesCases();
              }
            }
          }
        }
      }
    }
  }
  
  function checkNoInputCases()
  {
    if (!side1 || !side2 || !side3)
    {
      checkNoInput = checkNoInput * 1;
      checkNoInput++;
      
      if (checkNoInput > 1)
      {
        document.getElementById('dataComment').innerHTML = "This is another test for no input. It's valid when doing this for a different field. You have currently written " + checkNoInput + " tests for no input. Do you need more? Could you have got by with less?"
      } else {
        document.getElementById('dataComment').innerHTML = "Good. You have a test for no input."
      }
      return 0;
    } else {
      return 1;
    }
  }
  
  function checkWhitespaceCases()
  {
    while (side1.substring(0,1) == ' ') {
      side1 = side1.substring(1);
    }    
    while (side2.substring(0,1) == ' ') {
      side2 = side2.substring(1);
    }
    
    while (side3.substring(0,1) == ' ') {
      side3 = side3.substring(1);
    }
    
    if (side1.length == 0 || side2.length == 0 || side3.length == 0) {
      checkEmpty = checkEmpty * 1;
      checkEmpty++;
      
      if (checkEmpty > 1) {
        document.getElementById('dataComment').innerHTML = "This is another test for whitespace. You have currently written " + checkEmpty + " tests for whitespace. Do you need more? Could you have got by with less?"
      } else {
        document.getElementById('dataComment').innerHTML = "Good. You have a test for whitespace."
      }
      
      return 0;
    } else {
      return 1;
    }
  }
  
  function checkNonNumericCases()
  {
    var Chars = "0123456789-";
    checkNonNumeric = checkNonNumeric * 1;
    
    for (var i = 0; i < side1.length; i++) {
      if ((Chars.indexOf(side1.charAt(i)) == -1) || (Chars.indexOf(side2.charAt(i)) == -1) || (Chars.indexOf(side3.charAt(i)) == -1) )
      {
        checkNonNumeric++;
        
        if (checkNonNumeric > 1 ) {
          document.getElementById('dataComment').innerHTML = "This is another test for non-numeric characters. You have currently written " + checkNonNumeric + " tests for non-numeric characters. How many should you test? Is it necessary to have separate tests for every non-numeric character?"
        } else {
          document.getElementById('dataComment').innerHTML = "Good. You are testing for non-numeric characters."
        }
        return 0;
      }
    }
    return 1;
  }
  
  function checkNegativeCases()
  {
    if (side1Val < 0 || side2Val < 0 || side3Val < 0 )
    {
      negativeSide = negativeSide * 1;
      negativeSide++;
      
      if (negativeSide > 1 ) {
        document.getElementById('dataComment').innerHTML = "This is another test for negative side values. You have currently written " + negativeSide + " tests for negative sides. How many of these are necessarily required given that the calculation as a whole will react to any negative values?"
      } else {
        document.getElementById('dataComment').innerHTML = "Good. You are testing for negative side values."
      }
      return 0;
    } else {
      return 1;
    }
  }
  
  function checkZeroLengthCases()
  {
    if (side1Val == 0 || side2Val == 0 || side3Val == 0 )
    {
      zeroSide = zeroSide * 1;
      zeroSide++;
      
      if (zeroSides > 1 ) {
        document.getElementById('dataComment').innerHTML = "This is another test for side values of zero. You have currently written " + zeroSide + " tests for sides with a zero value. How many of these are relevant given the nature of the calculation being performed?"
      } else {
        document.getElementById('dataComment').innerHTML = "Good. You are testing for side values of zero."
      }
      return 0;
    } else {
      return 1;
    }
  }
  
  function checkInvalidTriangleCases()
  {
    if (side1Val + side2Val <= side3Val || side2Val + side3Val <= side1Val || side1Val + side3Val <= side2Val) {
      invalidSides = invalidSides * 1;
      invalidSides++;
      
      if (invalidSides > 1 ) {
        document.getElementById('dataComment').innerHTML = "This is another test for a mathematically impossible triangle. You have currently written " + invalidSides + " tests for such a situation. How many of these do you think you need to have?"
      } else {
        document.getElementById('dataComment').innerHTML = "Good. You are testing for invalid triangles, on the assumption of the theorem, which is that the addition of any two sides should always be greater than the third. This was a critical data condition."
      }
      return 0;
    } else {
      return 1;
    }
  }
  
  function checkLargeSideCases()
  {
    if (side1Val > 32767 || side2Val > 32767 || side3Val > 32767 ) {
      largeSides = largeSides * 1;
      largeSides++;
      
      if (largeSides > 1 ) {
        document.getElementById('dataComment').innerHTML = "This is another test for large sides to the a triangle. You have currently written " + largeSides + " tests for triangles with large sides. How many variations of 'large size' would realistically be required?"
      } else {
        document.getElementById('dataComment').innerHTML = "Good. You are testing for large sided triangles."
      }
      return 0;
    } else {
      return 1;
    }
  }
  
  function checkScaleneCases()
  {
    if (side1Val != side2Val && side1Val != side3Val && side2Val != side3Val) {
      checkScalene = checkScalene * 1;
      checkScalene++;
      
      if (checkScalene > 1 ) {
        document.getElementById('dataComment').innerHTML = "This is another test for scalene triangles. You have " + checkScalene + " tests now for scalene triangles."
      } else {
        document.getElementById('dataComment').innerHTML = "Good. You have made sure that a scalene triangle will work. This is a critical test."
      }
      return 0;
    } else {
      return 1;
    }
  }
  
  function checkEquilateralCases()
  {
    if (side1Val != side2Val && side1Val != side3Val && side2Val != side3Val) {
      checkEquilateral = checkEquilateral * 1;
      checkEquilateral++;
      
      if (checkEquilateral > 1 ) {
        document.getElementById('dataComment').innerHTML = "This is another test for equilateral triangles. You have " + checkEquilateral + " tests now for equilateral triangles."
      } else {
        document.getElementById('dataComment').innerHTML = "Good. You have made sure that an equilateral triangle will work. This is a critical test."
      }
      return 0;
    } else {
      return 1;
    }
  }
  
  function checkIsoscelesCases()
  {
    if (side1Val != side2Val && side1Val != side3Val && side2Val != side3Val) {
      checkIsosceles = checkIsosceles * 1;
      checkIsosceles++;
      
      if (checkIsosceles > 1 ) {
        document.getElementById('dataComment').innerHTML = "This is another test for isosceles triangles. You have " + checkIsosceles + " tests now for isosceles triangles."
      } else {
        document.getElementById('dataComment').innerHTML = "Good. You have made sure that an isosceles triangle will work. This is a critical test."
      }
      return 0;
    } else {
      return 1;
    }
  }
  
  function evalResults()
  {
    document.getElementById('response').innerHTML = "<strong>Results</strong>"
    document.getElementById('results').innerHTML = "";
    
    var scoreCount = 0;
    var noScoreCount = 0;
    
    scoreCount = scoreCount * 1;
    noScoreCount = noScoreCount * 1;
    
    if (checkNoInput == 0) {
      document.getElementById('results').innerHTML += "What about checking for no input? <br /><br />"
      noScoreCount++;
    }
    
    if (checkEmpty == 0) {
      document.getElementById('results').innerHTML += "What about checking for whitespace? <br /><br />"
      noScoreCount++;
    }
    
    if (checkNonNumeric == 0) {
      document.getElementById('results').innerHTML += "What about checking for non-numeric characters? <br /><br />"
      noScoreCount++;
    }
    
    if (negativeSide == 0) {
      document.getElementById('results').innerHTML += "What about checking for negative side values? <br /><br />"
      noScoreCount++;
    }
    
    if (zeroSide == 0) {
      document.getElementById('results').innerHTML += "What about checking for side values that are zero? <br /><br />"
      noScoreCount++;
    }
    
    if (invalidSides == 0) {
      document.getElementById('results').innerHTML += "What about checking for triangle values using a + b > c? That is a critical case. <br /><br />"
      noScoreCount++;
    }
    
    if (largeSides == 0) {
      document.getElementById('results').innerHTML += "What about checking for triangle with large sides? <br /><br />"
      noScoreCount++;
    }
    
    if (checkScalene == 0) {
      document.getElementById('results').innerHTML += "What about checking for a scalene triangle? That is a critical case. <br /><br />"
      noScoreCount++;
    }
    
    if (checkEquilateral == 0) {
      document.getElementById('results').innerHTML += "What about checking for an equilateral triangle? That is a critical case. <br /><br />"
      noScoreCount++;
    }
    
    if (checkIsosceles == 0) {
      document.getElementById('results').innerHTML += "What about checking for an isosceles triangle? That is a critical case. <br /><br />"
      noScoreCount++;
    }
    
    scoreCount = 10 - noScoreCount;
    
    if (scoreCount > 6) {
      document.getElementById('score').innerHTML = "Not bad. Your score is " + scoreCount + ". Could be worse."
    } else {
      document.getElementById('score').innerHTML = "Wow. Your score is " + scoreCount + ". You should be ashamed."
    }
  }
  
  function resetTest()
  {
    checkNoInput = 0;
    checkEmpty = 0;
    checkNonNumeric = 0;
    negativeSide = 0;
    zeroSide = 0;
    invalidSides = 0;
    largeSides = 0;
    checkScalene = 0;
    checkEquilateral = 0;
    checkIsosceles = 0;
    
    document.getElementById('response').innerHTML = " "
    document.getElementById('dataComment').innerHTML = " "
    document.getElementById('results').innerHTML = " "
    document.getElementById('score').innerHTML = " "
    
    document.getElementById('side1').value = ""
    document.getElementById('side2').value = ""
    document.getElementById('side3').value = ""
  }

</script>

<p>The triangle test is designed to check your ability to think about generating test data for a given condition.</p>

<p>Suppose your program accepts the three sides of a triangle as input. The program then outputs what type of triangle would be generated. Results might include the following:</p>

<ul>
<li>Scalene (no sides are same)</li>
<li>Isosceles (any two sides are same)</li>
<li>Equilateral (all the three sides are same)</li>
</ul>

<p>You have to come up with different test cases to test the application.</p>


<form>
<p><strong>Side 1:</strong> <input id="side1" type="text"></p>
<p><strong>Side 2:</strong> <input id="side2" type="text"></p>
<p><strong>Side 3:</strong> <input id="side3" type="text"></p>

<p><span id="response"> </span></p>

<input onclick="evalData()" value="Evaluate Test Data" type="button">
<input onclick="evalResults()" value="Evaluate Data Conditions" type="button">
<input onclick="resetTest()" value="Restart Test Condition" type="button">
</form>

<p><strong>Comments on Test Data:</strong></p>
<div id="dataComment"></div>

<p><strong>Comments on Data Conditions:</strong></p>
<div id="results"></div>

<p><strong>Test Score</strong></p>
<div id="score"></div>

</body>
</html>
