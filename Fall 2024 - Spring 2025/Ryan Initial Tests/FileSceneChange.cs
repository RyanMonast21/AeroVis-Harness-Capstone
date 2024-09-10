using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ChangeScenes : MonoBehaviour
{
	public void GoToFileSelectionScene()
	{
		SceneManager.LoadScene("FileSelectionScene");
	}
    public void GoToFileLibrary()
    {
        SceneManager.LoadScene("FileLibrary");
    }
    public void ReturnToMainMenu()
    {
        SceneManager.LoadScene("MainMenu");
    }

}