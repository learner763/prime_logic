import './App.css';
import {useState,useEffect, useRef} from 'react';
import { data, useNavigate } from 'react-router-dom';
function App() {

  const [login_menu,set_login_menu] = useState(true);
  const [email,set_email] = useState('');
  const [password,set_password] = useState('');
  const [fullname,set_fullname] = useState('');
  const dialogref=useRef(null);
  const [dialog_value,set_dialog_value]=useState('');
  const [ready,set_ready]=useState(false)
  const nav=useNavigate();

  function forgot_password()
  {
    set_dialog_value(
      <div>
        <input id='account_email' type='text' placeholder='Email of your account'></input>
        <label id='forgot_password_message'>Enter email to get your password</label>
        <button onClick={()=>
          {
            let forgot_password_message=document.getElementById('forgot_password_message')
            let account_email=document.getElementById('account_email').value
            if (!account_email.includes('@') || !account_email.includes('.') || account_email.split('@')[0].length===0 || account_email.split('@')[1].length===0 || account_email.split('@')[1].split('.')[0].length===0 || account_email.split('@')[1].split('.')[1].length===0)
            {
              forgot_password_message.innerHTML='Correct Email Format: you@domain.com'
            }
            else if(account_email.length===0 || account_email.length>30)
            {
              forgot_password_message.innerHTML='Email length Range: 1-30'
            }
            else{
              fetch('/forgot_password',{
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({account_email:account_email,token:localStorage.getItem('token'),email:localStorage.getItem('email')})
              })
              .then(responce=>responce.json())
              .then(data=>
                {
                  console.log(data)
                  if(!data.success)
                  {
                    forgot_password_message.innerHTML=data.message
                  }
                  else if(data.success)
                  {
                    if(data.verified)
                    {
                      forgot_password_message.innerHTML=`Your Password is ${data.password}`
                    }
                    else{
                      forgot_password_message.innerHTML=data.message
                    }
                  }
                }
              )
            }
          }
        }
        >Find Password</button>
        <button onClick={()=>dialogref.current.close()}>Back</button>
      </div>
    )
    dialogref.current.showModal()
  }

  useEffect(()=>
  {
    if(localStorage.getItem('email') || localStorage.getItem('token'))
    {
      fetch('/remember_me',{
        method:'POST',
        headers:{
          'Content-Type':'application/json'
        },
        body:JSON.stringify({
          email:localStorage.getItem('email'),
          token:localStorage.getItem('token')
        })
      })
      .then(responce=>responce.json())
      .then(data=>
      {
        if(data.success)
        {
          set_email(data.email)
          set_password(data.password)
          if(data.through=='email')
          {
          set_dialog_value(
            <div >
              <label>{data.message}</label>
              <input type='text' id='input_otp' placeholder='Enter OTP'></input>
              <label id='otp_message'>Enter OTP received on your email address</label>
              <button onClick={()=>
                {
                  fetch('/verify_otp',{
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify({otp:document.getElementById('input_otp').value,email:localStorage.getItem('email')})
                  })
                  .then(res=>res.json())
                  .then(data=>
                  {
                    if(data.success)
                    {
                      localStorage.removeItem('email')
                      localStorage.setItem('logged_in',true)
                      localStorage.setItem('token',data.token)
                      nav('/dashboard')
                    }
                    else
                    {
                      if(data.InvalidToken)
                      {
                        set_dialog_value(
                          <div>
                            <label>{data.InvalidToken}</label>
                            <button onClick={()=>dialogref.current.close()}>Close</button>
                        </div>
                        )
                        set_login_menu(true)
                      }
                      else
                      {
                        document.getElementById('otp_message').innerHTML=data.message
                      }
                    }
                  })
                }
              }>Submit</button>
              <button onClick={()=>dialogref.current.close()}>Back</button>
            </div>
            )
            dialogref.current.showModal()
          }
        }
        else{
          if(localStorage.getItem('email'))
          {
            localStorage.removeItem('email')
          }
        }
        set_ready(true)
      })
    }
    else{
      set_ready(true)
    }
  },[])

  useEffect(()=>
  {
    set_fullname('')
    set_email('')
    set_password('')
  },[login_menu])

  return (
    <>
      <div className="circle" style={{display:ready?'none':'flex'}}>    
        <div className='loader' style={{width:'50px',height:'50px',borderRadius:'50%',border:'5px solid white',borderTop:'5px solid #ff008e',animation:'spin 1s linear infinite'}}></div>
      </div>      
      <div className='parent' style={{display:ready?'flex':'none'}}>
        <div className='children'>
          <div className='child1'>
            <button>December 1-3, 2025</button>
            <label>TechFest</label>
            <label>2025</label>
            <label>Where Innovation Meets Competition</label>
            <div>
              <span>
                <i className="fa-solid fa-gamepad" style={{color:'lime'}}></i>
                <label>Games</label>
              </span>
              <span>
                <i className="fa-solid fa-microchip" style={{color:'yellow'}}></i>
                <label>Electronics</label>
              </span>
              <span>
                <i className="fa-solid fa-code" style={{color:'deepskyblue'}}></i>
                <label>Coding</label>
              </span>
            </div>
          </div>
          <div className='child2'>
            <label>Welcome Back</label>
            <label>Login to register for events and track your participation</label>
            <label style={{fontWeight:'bold'}}>
              <span style={{backgroundColor:login_menu?'white':'#ff008e',color:login_menu?'#ff008e':'white'}}
                onClick={()=>login_menu?'':set_login_menu(true)}>Login</span>
              <span style={{backgroundColor:!login_menu?'white':'#ff008e',color:!login_menu?'#ff008e':'white'}}
                onClick={()=>login_menu?set_login_menu(false):''}>Sign Up</span>
            </label>
            <label style={{display:login_menu?'none':'flex'}}>Full Name</label>
            <input onChange={(e)=>set_fullname(e.target.value.replace(/[^a-zA-Z\_]/g, ""))} value={fullname} style={{display:login_menu?'none':'flex'}} placeholder='Akhta_Lava'></input>
            <label>Email</label>
            <input onChange={(e)=>set_email(e.target.value.replace(/[^a-zA-Z0-9_@.+]/g, ""))} value={email} placeholder='akhtarlava@gmail.com'></input>
            <label>
              <span>Password</span>
              <span onClick={()=>forgot_password()} style={{cursor:'pointer',display:login_menu?'flex':'none'}}>Forgot Password?</span>
            </label>
            <input onChange={(e)=>set_password(e.target.value.replaceAll(' ',''))} value={password} type='password' placeholder='nahi-bataunga'></input>
            <button onClick={(e)=>
              {
                if(e.target.disabled){return}
                e.target.disabled=true
                if(!login_menu && (email.length>30 || email.length===0 || password.length>12 || password.length===0 || fullname.length>12 || fullname.length===0))
                {
                  set_dialog_value(
                    <div>
                      <label>Email length Range : 1:30,Password & Name length Range : 1:12</label>
                      <button onClick={()=>dialogref.current.close()}>Close</button>
                    </div>
                  )
                  dialogref.current.showModal()
                }
                else if(login_menu && (email.length>30 || email.length===0 || password.length>12 || password.length===0))
                {
                  set_dialog_value(
                    <div>
                      <label>Email length Range : 1:30,Password length Range : 1:12</label>
                      <button onClick={()=>dialogref.current.close()}>Close</button>
                    </div>
                  )
                  dialogref.current.showModal()
                }
                else if (!email.includes('@') || !email.includes('.') || email.split('@')[0].length===0 || email.split('@')[1].length===0 || email.split('@')[1].split('.')[0].length===0 || email.split('@')[1].split('.')[1].length===0)
                {
                  set_dialog_value(
                    <div>
                      <label>Correct Email Format: you@domain.com</label>
                      <button onClick={()=>dialogref.current.close()}>Close</button>
                    </div>)
                  dialogref.current.showModal()
                }
                else{
                  fetch('/login',{
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify({action:login_menu,email:email,password:password,fullname:fullname,token:localStorage.getItem('token')})
                  })
                  .then(res=>res.json())
                  .then(data=>
                  {
                    console.log(data)
                    if(data.success)
                    {
                      if(data.verified)
                      {
                        localStorage.setItem('logged_in',true)
                        localStorage.setItem('token',data.token)
                        nav('/dashboard')
                      }
                      else if(data.email)
                      {
                        localStorage.setItem('email',data.email)
                        set_dialog_value(
                          <div>
                            <label>{data.message}</label>
                            <input type='text' id='input_otp' placeholder='Enter OTP'></input>
                            <label id='otp_message'>Enter OTP received on your email address</label>
                            <button onClick={()=>
                              {
                                fetch('/verify_otp',{
                                  method:'POST',
                                  headers:{'Content-Type':'application/json'},
                                  body:JSON.stringify({otp:document.getElementById('input_otp').value,'email':data.email})
                                })
                                .then(res=>res.json())
                                .then(data=>
                                {
                                  if(data.success)
                                  {
                                    localStorage.setItem('token',data.token)
                                    localStorage.setItem('logged_in',true)
                                    localStorage.removeItem('email')
                                    nav('/dashboard')
                                  }
                                  else
                                  {
                                    document.getElementById('otp_message').innerHTML=data.message
                                  }
                                })
                              }
                            }>Submit</button>
                            <button onClick={()=>dialogref.current.close()}>Back</button>
                          </div>
                        )
                        dialogref.current.showModal()
                      }
                    }
                    else{
                      dialogref.current.showModal()
                      set_dialog_value(
                        <div >
                          <label>{data.message}</label>
                          <button onClick={()=>dialogref.current.close()}>Close</button>
                        </div>
                      )
                    }
                  })
                }
              }
            }
            >{login_menu?'Login':'Create Account'}</button>
          </div>

        </div>
        <dialog ref={dialogref} style={{color:'white',borderRadius:'10px',backgroundColor:'#020618'}}>{dialog_value} </dialog>
      </div>
    </>
  );
}

export default App;
