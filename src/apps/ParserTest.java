package nostalgic.textadv.voxam;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;
import org.junit.After;

public class ParserTest {
    private Parser parser;
    private Command command;

    @Before
    public void setUp() {
        parser = new Parser();
    }

    @Test
    public void parseIntransitiveVerb() {
        command = parser.parse("wait");
        assertFalse("Should be no direct object.", command.hasDirectObject());
        assertFalse("Should be no indirect object.", command.hasIndirectObject());
        assertNull("Should be no direct object.", command.getDirectObject());
        assertNull("Should be no indirect object.", command.getIndirectObject());

        assertEquals("wait", command.getVerb());
        assertEquals("Success", command.getMessage());
    }

    @Test
    public void parseTransitiveVerb() {
        command = parser.parse("take sword");
        assertTrue("Should have a direct object.", command.hasDirectObject());
        assertFalse("Should have no directive.", command.hasDirective());

        assertEquals("take", command.getVerb());
        assertEquals("sword", command.getDirectObject());
        assertEquals("Success", command.getMessage());
    }

    @Test
    public void parseTransitiveVerbWithIndirectObject() {
        command = parser.parse("dig hole with shovel");
        assertTrue("Should have a direct object.", command.hasDirectObject());
        assertTrue("Should have an indirect object.", command.hasIndirectObject());

        assertEquals("dig", command.getVerb());
        assertEquals("hole", command.getDirectObject());
        assertEquals("shovel", command.getIndirectObject());
        assertEquals("Success", command.getMessage());
    }

    @Test
    public void parseTransitiveVerbWithIndirectObjectAndArticles() {
        command = parser.parse("dig a hole with the shovel");

        assertEquals("dig", command.getVerb());
        assertEquals("hole", command.getDirectObject());
        assertEquals("shovel", command.getIndirectObject());
        assertEquals("Success", command.getMessage());
    }

    @Test
    public void parseTransitiveVerbWithArticle() {
        command = parser.parse("take the sword");
        assertTrue("Should have a direct object.", command.hasDirectObject());

        assertEquals("take", command.getVerb());
        assertEquals("sword", command.getDirectObject());
        assertEquals("Success", command.getMessage());
    }

    @Test
    public void parseTransitiveVerbWithAdjective() {
        command = parser.parse("take the golden sword");
        assertTrue("Should have a direct object.", command.hasDirectObject());

        assertEquals("take", command.getVerb());
        assertEquals("golden sword", command.getDirectObject());
        assertEquals("Success", command.getMessage());
    }

    @Test
    public void parseTransitiveVerbWithArticleInDirectObject() {
        command = parser.parse("take the golden sword of the ancients");
        assertTrue("Should have a direct object.", command.hasDirectObject());

        assertEquals("take", command.getVerb());
        assertEquals("golden sword of the ancients", command.getDirectObject());
        assertEquals("Success", command.getMessage());
    }

    @Test
    public void parseActionsWithDirective() {
        command = parser.parse("floyd, wait");
        assertTrue("Should have directive.", command.hasDirective());

        assertEquals("floyd", command.getDirective());
        assertEquals("wait", command.getVerb());

        command = parser.parse("floyd, take the golden sword");
        assertTrue("Should have directive.", command.hasDirective());

        assertEquals("floyd", command.getDirective());
        assertEquals("take", command.getVerb());
        assertEquals("golden sword", command.getDirectObject());
    }

    @Test
    public void parseStripPunctuation() {
        command = parser.parse("inventory.");

        assertEquals("inventory", command.getVerb());
        assertEquals("Success", command.getMessage());

        command = parser.parse("escape!");

        assertEquals("escape", command.getVerb());
        assertEquals("Success", command.getMessage());

        command = parser.parse("take sword...");

        assertEquals("take", command.getVerb());
        assertEquals("sword", command.getDirectObject());
        assertEquals("Success", command.getMessage());
    }

    @Test
    public void parseNoCommand() {
        command = parser.parse("");

        assertNull("Should be no verb.", command.getVerb());
        assertNull("Should be no direct object.", command.getDirectObject());
        assertEquals("No command to parse.", command.getMessage());
    }

    @Test
    public void parseNoCommandAfterScrub() {
        command = parser.parse(".");

        assertNull("Should be no verb.", command.getVerb());
        assertNull("Should be no direct object.", command.getDirectObject());
        assertEquals("No command to parse.", command.getMessage());
    }

    @After
    public void tearDown() {
        parser = null;
    }
}
