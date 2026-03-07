import { useState, useCallback, useEffect } from 'react';
import {Grid, Typography, Card, Textarea, IconButton, Select, Option, Stack, CircularProgress } from '@mui/joy';
import SubdirectoryArrowLeftIcon from '@mui/icons-material/SubdirectoryArrowLeft';
import habitApi from '../../habitApi';
import PropTypes from 'prop-types';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import SaveAltIcon from '@mui/icons-material/SaveAlt';
import SettingsIcon from '@mui/icons-material/Settings';
export default function MentorChat({habitId}){
    const [inputValue, setInputValue] = useState('');
    const [messages, setMessages] = useState([]);
    const [toggle, setToggle] = useState(false);
    const [setupMenu , setSetupMenu ] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [chatError, setChatError] = useState(null);

    const [configId, setConfigId] = useState(0)
    const [communicationStyle, setCommunicationStyle] = useState("");
    const [languagePreference, setLanguagePreference] = useState("");
    const [personalityPrompt, setPersonalityPrompt] = useState("");


    useEffect(() => {
        const fetchMentorConfg = async() =>{
            let habitId = document.cookie.split('; ').find(row => row.startsWith('habitId='));
            habitId = habitId.split('=')[1];
            const configData = await habitApi.getConfig(habitId);
            console.log(configData);
            setCommunicationStyle(configData.data.communication_style);
            setLanguagePreference(configData.data.language_preference);
            setPersonalityPrompt(configData.data.personality_prompt);
            setConfigId(configData.data.id);
        };
        fetchMentorConfg();
    },[])

    const handleInputChange = useCallback((event) => {
        const { value } = event.target;
        setInputValue(value);
    }, []);
    const handleMessageSend = async(event) =>{
        event.preventDefault();
        if (!inputValue.trim() || isLoading) return;
        let lastMessage;

        setMessages(prevMessages => {
            const newMessage = inputValue;
            const updatedMessages = [...prevMessages, newMessage];
            lastMessage = updatedMessages[updatedMessages.length - 1]
            setInputValue(''); 
            return updatedMessages;
        });
        console.log(lastMessage);

        const messageData = {
            "message": lastMessage
        };
        setIsLoading(true);
        setChatError(null);
        try {
            const response = await habitApi.postMessage(habitId, messageData)
            setMessages(prevMessages => {
                const newMessage = response.data;
                const updatedMessages = [...prevMessages, newMessage];
                return updatedMessages;
            });
        } catch {
            setChatError("Failed to get a response. Please try again.");
        } finally {
            setIsLoading(false);
        }
    }
    const toggleChat = () =>{
        setToggle(!toggle)
    }

    const handleCSelectChange = (e, newValue) => {
        setCommunicationStyle(newValue);
    };
    const handleLSelectChange = (e, newValue) => {
        setLanguagePreference(newValue);
    };
    const saveConfig = async() => {
        const data = {
            habit_tracker: habitId,
            communication_style: communicationStyle,
            language_preference: languagePreference,
            personality_prompt:  personalityPrompt
        }
        await habitApi.putConfig(configId, data);
        setSetupMenu(!setupMenu);
    }
    return (
        <>
            {toggle ? <>
                <IconButton size='sm' onClick={toggleChat}sx={{height:'2px', width:'100%'}}><MoreHorizIcon></MoreHorizIcon></IconButton>
            </> : <>
            <Card sx={{height: "500px"}} size='sm' >
                <IconButton  sx={{height:'2px'}}  onClick={toggleChat}><MoreHorizIcon></MoreHorizIcon></IconButton>

                <Card variant="soft" sx={{
                    height: "500px",
                    overflowY: 'auto',
                    border: '1px solid',
                    borderColor: '#CDD7E1',
                    borderRadius: '4px', 
    
                }}>
                    {setupMenu ? <>
                        <Card variant='outlined' sx={{
                        height: "250px",
                        width: "500px",
                        display: 'flex',
                        flexDirection: 'column',
                        position: 'absolute', 
                        top: '50%', left: '50%', 
                        transform: 'translate(-50%, -50%)'
                        }}>
                            <Grid container spacing={2} alignItems="stretch">
                                <Grid item xs={10.5}>
                                    <Typography level='h4' align="left">Mentor Config</Typography>
                                </Grid>
                                <Grid item xs={1.5}>
                                    <IconButton onClick={saveConfig}><SaveAltIcon></SaveAltIcon></IconButton>
                                </Grid>
                            </Grid>
                            <Card>
                                <Grid container spacing={2} alignItems="stretch">
                                    <Grid item xs={6}>
                                        <Stack></Stack>
                                        <Typography level='title-md' align="left">Communication Style:</Typography>
                                        <Select
                                            value={communicationStyle}
                                            onChange={handleCSelectChange}
                                            slotProps={{
                                            listbox: {
                                            placement: 'bottom-start',
                                            },
                                        }}>
                                            <Option value="motivational">Motivational: Providing uplifting messages to inspire action.</Option>
                                            <Option value="problem-solving">Problem-Solving: Offering practical strategies to overcome challenges.</Option>
                                            <Option value="collaborative">Collaborative: Encouraging user participation in decision-making.</Option>
                                            <Option value="reflective">Reflective: Promoting introspection and self-discovery through questions.</Option>
                                        </Select>
                                        <Typography level='title-md' align="left">Language Preferences:</Typography>
                                        <Select                                
                                        value={languagePreference}
                                        onChange={handleLSelectChange}
                                        slotProps={{
                                            listbox: {
                                            placement: 'bottom-start',
                                            },
                                        }}>
                                            <Option value="informative">Informative: Providing factual and educational content.</Option>
                                            <Option value="supportive">Supportive: Delivering empathetic and comforting messages.</Option>
                                            <Option value="encouraging">Encouraging: Offering words of empowerment and positivity.</Option>
                                            <Option value="assertive">Assertive: Providing firm guidance and direction for accountability.</Option>
                                        </Select>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography level='title-md' align="left">Mentor Personality Prompt:</Typography>
                                        <Textarea minRows={4}  value={personalityPrompt} onChange={(e) => setPersonalityPrompt(e.target.value)}></Textarea>
                                    </Grid>
                                </Grid>
                            </Card>
                        </Card>
                    </> : <></>}
                    <Grid container spacing={1} alignItems="stretch">
                        <Grid item xs={11.5}>
                        
                        {!setupMenu ? messages.map((message, index) => (
                            (index ) % 2 === 0 ? <>
                            
        
                                <Typography key={index} align="left" level='body-lg'> <strong>./msg/neacsu-000{index}/</strong> {message}</Typography>
                            </> : <>
                                <Typography key={index} align="left" level='body-lg'><strong>./msg/mind-sync-000{index}/</strong> {message}</Typography>
                            </>
                        )) : <></>}
                        {!setupMenu && isLoading && (
                            <Stack direction="row" spacing={1} alignItems="center" sx={{ my: 0.5 }}>
                                <Typography level='body-lg'><strong>./msg/mind-sync-generating/</strong></Typography>
                                <CircularProgress size="sm" />
                            </Stack>
                        )}
                        {!setupMenu && chatError && (
                            <Typography level='body-sm' color="danger" sx={{ my: 0.5 }}>{chatError}</Typography>
                        )}
                        </Grid>
                        <Grid item xs={.5}>
                            
                            {!setupMenu ? <IconButton onClick={() => setSetupMenu(!setupMenu)}><SettingsIcon></SettingsIcon></IconButton> : <></>}
                        </Grid>
                    </Grid>
                    
                </Card>
                <form>
                    <Grid container spacing={1} alignItems="stretch">
                        
                            <Grid item xs={11.55}>
                                {setupMenu ? <Textarea minRows={3} disabled/>:<Textarea minRows={3} onBlur={(e) => handleInputChange(e)} placeholder={"Send a Message!"} value={inputValue} onChange={(e) => setInputValue(e.target.value)} />}
                                {/* <Textarea minRows={3} onBlur={(e) => handleInputChange(e)} placeholder={"Send a Message!"} value={inputValue} onChange={(e) => setInputValue(e.target.value)} /> */}
                            </Grid>
                            <Grid item xs={.45}>
                                <IconButton sx={{height:"87px"}}variant='outlined' onClick={handleMessageSend} disabled={isLoading}><SubdirectoryArrowLeftIcon></SubdirectoryArrowLeftIcon></IconButton>
                            </Grid>
                        
                    </Grid>
                </form>
    
            </Card>
            </>  }
            
        </>
    )
}
MentorChat.propTypes = {
    habitId: PropTypes.number.isRequired,
};