from cx_Freeze import setup, Executable 
import sys, os

sys.setrecursionlimit(100000)


#Fix to the DLL problem, the fix is just to include all mission DLLs.
mkl_dll_path = r"C:\Users\swak\AppData\Local\Programs\Python\Python311\Library\bin"



build_exe_options = {
    "packages": ["os", "easyocr", "customtkinter"],  # Add any required packages
    "include_files": [("model", "model"), ("image_placeholder.png", "image_placeholder.png"),
                      ("favicon.ico", "favicon.ico"),
                      (os.path.join(mkl_dll_path, "libiomp5md.dll"), "libiomp5md.dll"),
                      (os.path.join(mkl_dll_path, "mkl_avx.1.dll"), "mkl_avx.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_avx2.1.dll"), "mkl_avx2.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_avx512.1.dll"), "mkl_avx512.1.dll"),                      
                      (os.path.join(mkl_dll_path, "mkl_blacs_ilp64.1.dll"), "mkl_blacs_ilp64.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_blacs_intelmpi_ilp64.1.dll"), "mkl_blacs_intelmpi_ilp64.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_blacs_intelmpi_lp64.1.dll"), "mkl_blacs_intelmpi_lp64.1.dll"),                      
                      (os.path.join(mkl_dll_path, "mkl_blacs_lp64.1.dll"), "mkl_blacs_lp64.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_blacs_mpich2_ilp64.1.dll"), "mkl_blacs_mpich2_ilp64.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_blacs_mpich2_lp64.1.dll"), "mkl_blacs_mpich2_lp64.1.dll"),                      
                      (os.path.join(mkl_dll_path, "mkl_blacs_msmpi_ilp64.1.dll"), "mkl_blacs_msmpi_ilp64.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_blacs_msmpi_lp64.1.dll"), "mkl_blacs_msmpi_lp64.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_cdft_core.1.dll"), "mkl_cdft_core.1.dll"),                      
                      (os.path.join(mkl_dll_path, "mkl_core.1.dll"), "mkl_core.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_def.1.dll"), "mkl_def.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_intel_thread.1.dll"), "mkl_intel_thread.1.dll"),                     
                      (os.path.join(mkl_dll_path, "mkl_mc.1.dll"), "mkl_mc.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_mc3.1.dll"), "mkl_mc3.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_msg.dll"), "mkl_msg.dll"),                      
                      (os.path.join(mkl_dll_path, "mkl_pgi_thread.1.dll"), "mkl_pgi_thread.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_rt.1.dll"), "mkl_rt.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_scalapack_ilp64.1.dll"), "mkl_scalapack_ilp64.1.dll"),                      
                      (os.path.join(mkl_dll_path, "mkl_scalapack_lp64.1.dll"), "mkl_scalapack_lp64.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_sequential.1.dll"), "mkl_sequential.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_tbb_thread.1.dll"), "mkl_tbb_thread.1.dll"),                      
                      (os.path.join(mkl_dll_path, "mkl_vml_avx.1.dll"), "mkl_vml_avx.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_vml_avx2.1.dll"), "mkl_vml_avx2.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_vml_avx512.1.dll"), "mkl_vml_avx512.1.dll"),                      
                      (os.path.join(mkl_dll_path, "mkl_vml_cmpt.1.dll"), "mkl_vml_cmpt.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_vml_def.1.dll"), "mkl_vml_def.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_vml_mc.1.dll"), "mkl_vml_mc.1.dll"),                      
                      (os.path.join(mkl_dll_path, "mkl_vml_mc2.1.dll"), "mkl_vml_mc2.1.dll"),
                      (os.path.join(mkl_dll_path, "mkl_vml_mc3.1.dll"), "mkl_vml_mc3.1.dll"),
                      ],  # Copy the model folder to the build
}


setup(name = "Tawgeehat R2aseya" , 
      version = "0.1" , 
      description = "" ,
      options={"build_exe": build_exe_options},
      executables = [Executable(script="snipper.py", target_name='Tawgeehat R2aseya', icon='favicon.ico')]) 