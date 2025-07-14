package es.gameshelf.domain.services;

import es.gameshelf.domain.*;
import es.gameshelf.domain.interfaces.repository.IGameRepository;
import es.gameshelf.domain.interfaces.service.IGameService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Set;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class GameService implements IGameService {

    /**
     * Properties
     */
    IGameRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IGameRepository repository) {
        this.repository = repository;
    }

    @Override
    public Game add(String title, String releaseDate, String slug, String cover, int externalRating,
                    Set<Developer> developerSet, Set<Publisher> publisherSet, Set<Format> formatSet,
                    Set<Platform> platformSet, Set<Genre> genreSet) {
        Game item = new Game();
        item.setTitle(title);
        item.setReleaseDate(releaseDate);
        item.setSlug(slug);
        item.setCover(cover);
        item.setExternalRating(externalRating);
        item.setDeveloperSet(developerSet);
        item.setPublisherSet(publisherSet);
        item.setFormatSet(formatSet);
        item.setPlatformSet(platformSet);
        item.setGenreSet(genreSet);

        return repository.save(item);
    }

    @Override
    public List<Game> findAll() {
        return repository.findAll();
    }

    @Override
    public Game findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Game findByTitle(String title) {
        return repository.findByTitle(title);
    }

    @Override
    public Game findBySlug(String slug) {
        return repository.findBySlug(slug);
    }

    @Override
    public List<Game> findAllByYear(Integer year) {
        return repository.findAllByYear(year);
    }

    @Override
    public List<Game> findAllByPlatform(Platform platform) {
        return repository.findAllByPlatform(platform);
    }

    @Override
    public List<Game> findAllByDeveloper(Developer developer) {
        return repository.findAllByDeveloper(developer);
    }

    @Override
    public List<Game> findAllByPublisher(Publisher publisher) {
        return repository.findAllByPublisher(publisher);
    }

    @Override
    public List<Game> findAllByGenre(Genre genre) {
        return repository.findAllByGenre(genre);
    }

    @Override
    public List<Game> findAllByFormat(Format format) {
        return repository.findAllByFormat(format);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Game update(Integer id, String title, String releaseDate, String slug, String cover, int externalRating,
                       Set<Developer> developerSet, Set<Publisher> publisherSet, Set<Format> formatSet,
                       Set<Platform> platformSet, Set<Genre> genreSet) {
        Game item = new Game(id);
        item.setTitle(title);
        item.setReleaseDate(releaseDate);
        item.setSlug(slug);
        item.setCover(cover);
        item.setExternalRating(externalRating);
        item.setDeveloperSet(developerSet);
        item.setPublisherSet(publisherSet);
        item.setFormatSet(formatSet);
        item.setPlatformSet(platformSet);
        item.setGenreSet(genreSet);

        return repository.update(item);
    }
}
